from pygeoapi.api import (
    SYSTEM_LOCALE
)
import json
import logging
import urllib.parse
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Tuple

from pygeoapi import l10n
from pygeoapi.api import (
    APIRequest, API, SYSTEM_LOCALE, F_JSON, FORMAT_TYPES, F_HTML
)
from pygeoapi.process.base import (
    JobNotFoundError, ProcessorExecuteError
)
from pygeoapi.process.manager.base import Subscriber
from pygeoapi.util import (
    render_j2_template, JobStatus, RequestedProcessExecutionMode,
    to_json, DATETIME_FORMAT)
from pygeoapi_prefect.schemas import (
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

    try:
        logger.debug('Scheduling process')

        result = api.manager.schedule_process(
            process_id, data_dict)
        schedule_id, mime_type, status = result

        if api.manager.is_async:
            headers['Location'] = f'{api.base_url}/schedule/{schedule_id}'

    except ProcessorExecuteError as err:
        return api.get_exception(
            err.http_status_code, headers,
            request.format, err.ogc_exception_code, err.message)

    response = {}
    if status == JobStatus.failed:
        response = {}
    elif status not in (JobStatus.failed, JobStatus.accepted):
        response = {"scheduling_id": schedule_id}

    if requested_response == 'raw':
        headers['Content-Type'] = mime_type

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