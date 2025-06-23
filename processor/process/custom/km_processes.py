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
        schedule_id, mime_type, output, status, headers = result

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


def get_schedules(api: API, request: APIRequest, schedule_id=None) -> Tuple[dict, int, str]:
    """
    Get process schedules

    :param request: A request object
    :param schedule_id: id of schedule

    :returns: tuple of headers, status code, content
    """

    headers = request.get_response_headers(SYSTEM_LOCALE,
                                           **api.api_headers)
    logger.debug('Processing limit parameter')
    try:
        limit = int(request.params.get('limit'))

        if limit <= 0:
            msg = 'limit value should be strictly positive'
            return api.get_exception(
                HTTPStatus.BAD_REQUEST, headers, request.format,
                'InvalidParameterValue', msg)
    except TypeError:
        limit = int(api.config['server']['limit'])
        logger.debug('returning all schedules')
    except ValueError:
        msg = 'limit value should be an integer'
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format,
            'InvalidParameterValue', msg)

    logger.debug('Processing offset parameter')
    try:
        offset = int(request.params.get('offset'))
        if offset < 0:
            msg = 'offset value should be positive or zero'
            return api.get_exception(
                HTTPStatus.BAD_REQUEST, headers, request.format,
                'InvalidParameterValue', msg)
    except TypeError as err:
        logger.warning(err)
        offset = 0
    except ValueError:
        msg = 'offset value should be an integer'
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format,
            'InvalidParameterValue', msg)

    if schedule_id is None:
        schedules_data = api.manager.get_schedules(limit=limit, offset=offset)
        # TODO: For pagination to work, the provider has to do the sorting.
        #       Here we do sort again in case the provider doesn't support
        #       pagination yet and always returns all jobs.
        schedules = sorted(schedules_data['schedules'],
                      key=lambda k: k['created'],
                      reverse=True)
        numberMatched = schedules_data['numberMatched']

    else:
        try:
            schedules = [api.manager.get_schedule(schedule_id)]
        except JobNotFoundError:
            return api.get_exception(
                HTTPStatus.NOT_FOUND, headers, request.format,
                'InvalidParameterValue', schedule_id)
        numberMatched = 1

    serialized_schedules = {
        'schedules': [],
        'links': [{
            'href': f"{api.base_url}/schedules?f={F_JSON}",
            'rel': request.get_linkrel(F_JSON),
            'type': FORMAT_TYPES[F_JSON],
            'title': l10n.translate('Schedule list as JSON', request.locale)
        }]
    }
    for schedule_ in schedules:
        schedule2 = {
            'type': 'process',
            'processID': schedule_['process_id'],
            'scheduleID': schedule_['schedule_id'],
            'jobIDs': schedule_['job_ids'],
            'status': schedule_['status'],
            'scheduleCreated': schedule_['created'],
            'scheduleUpdated': schedule_['updated'],
            'scheduleActive': schedule_['active'],
            'scheduleCron': schedule_['cron']
        }

        serialized_schedules['schedules'].append(schedule2)

    serialized_query_params = ''
    for k, v in request.params.items():
        if k not in ('f', 'offset'):
            serialized_query_params += '&'
            serialized_query_params += urllib.parse.quote(k, safe='')
            serialized_query_params += '='
            serialized_query_params += urllib.parse.quote(str(v), safe=',')

    uri = f'{api.base_url}/jobs'

    if offset > 0:
        prev = max(0, offset - limit)
        serialized_schedules['links'].append(
            {
                'href': f'{uri}?offset={prev}{serialized_query_params}',
                'type': FORMAT_TYPES[F_JSON],
                'rel': 'prev',
                'title': l10n.translate('Items (prev)', request.locale),
            })

    next_link = False

    if numberMatched > (limit + offset):
        next_link = True
    elif len(schedules) == limit:
        next_link = True

    if next_link:
        next_ = offset + limit
        next_href = f'{uri}?offset={next_}{serialized_query_params}'
        serialized_schedules['links'].append(
            {
                'href': next_href,
                'rel': 'next',
                'type': FORMAT_TYPES[F_JSON],
                'title': l10n.translate('Items (next)', request.locale),
            })

    return headers, HTTPStatus.OK, to_json(serialized_schedules,
                                           api.pretty_print)
