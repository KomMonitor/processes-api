from http import HTTPStatus
from typing import (
    Any,
    Tuple
)
import json
import logging
from .. import base
from pygeoapi.util import (
    JobStatus, RequestedProcessExecutionMode, to_json
)
from pygeoapi.process.base import (
    ProcessorExecuteError
)
from pygeoapi.api import (
    APIRequest, API, SYSTEM_LOCALE
)
from pygeoapi.process.manager.base import Subscriber
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.schemas import (
    ExecuteRequest,
    ProcessExecutionMode,
    RequestedProcessExecutionMode,
)

logger = logging.getLogger(__name__)

def schedule_process(api: API, request: APIRequest,
                    process_id) -> Tuple[dict, int, str]:
    """
    Execute process

    :param request: A request object
    :param process_id: id of process

    :returns: tuple of headers, status code, content
    """

    # Responses are always in US English only
    headers = request.get_response_headers(SYSTEM_LOCALE,
                                           **api.api_headers)
    if process_id not in api.manager.processes:
        msg = 'identifier not found'
        return api.get_exception(
            HTTPStatus.NOT_FOUND, headers,
            request.format, 'NoSuchProcess', msg)

    data = request.data
    if not data:
        # TODO not all processes require input, e.g. time-dependent or
        #      random value generators
        msg = 'missing request data'
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format,
            'MissingParameterValue', msg)

    try:
        # Parse bytes data, if applicable
        data = data.decode()
        logger.debug(data)
    except (UnicodeDecodeError, AttributeError):
        pass

    try:
        data = json.loads(data)
    except (json.decoder.JSONDecodeError, TypeError):
        # Input does not appear to be valid JSON
        msg = 'invalid request data'
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format,
            'InvalidParameterValue', msg)

    data_dict = data.get('inputs', {})
    logger.debug(data_dict)

    requested_outputs = data.get('outputs')
    logger.debug(f'outputs: {requested_outputs}')

    requested_response = data.get('response', 'raw')

    subscriber = None
    subscriber_dict = data.get('subscriber')
    if subscriber_dict:
        try:
            success_uri = subscriber_dict['successUri']
        except KeyError:
            return api.get_exception(
                HTTPStatus.BAD_REQUEST, headers, request.format,
                'MissingParameterValue', 'Missing successUri')
        else:
            subscriber = Subscriber(
                # NOTE: successUri is mandatory according to the standard
                success_uri=success_uri,
                in_progress_uri=subscriber_dict.get('inProgressUri'),
                failed_uri=subscriber_dict.get('failedUri'),
            )

    try:
        execution_mode = RequestedProcessExecutionMode(
            request.headers.get('Prefer', request.headers.get('prefer'))
        )
    except ValueError:
        execution_mode = None
    try:
        logger.debug('Scheduling process')

        result = api.manager.schedule_process(
            process_id, data_dict, execution_mode=execution_mode)
        job_id, mime_type, outputs, status, additional_headers = result
        headers.update(additional_headers or {})

        if api.manager.is_async:
            headers['Location'] = f'{api.base_url}/jobs/{job_id}'

    except ProcessorExecuteError as err:
        return api.get_exception(
            err.http_status_code, headers,
            request.format, err.ogc_exception_code, err.message)

    response = {}
    if status == JobStatus.failed:
        response = outputs

    if requested_response == 'raw':
        headers['Content-Type'] = mime_type
        response = outputs
    elif status not in (JobStatus.failed, JobStatus.accepted):
        response = outputs

    if status == JobStatus.accepted:
        http_status = HTTPStatus.CREATED
    elif status == JobStatus.failed:
        http_status = HTTPStatus.BAD_REQUEST
    else:
        http_status = HTTPStatus.OK

    if mime_type == 'application/json' or requested_response == 'document':
        response2 = to_json(response, api.pretty_print)
    else:
        response2 = response

    return headers, http_status, response2