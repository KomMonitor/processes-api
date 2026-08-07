from authlib.oauth2.rfc6750 import InsufficientScopeError
from pygeoapi.api import (
    SYSTEM_LOCALE, apply_gzip
)
import json
import logging
import urllib.parse
import os
from http import HTTPStatus
from typing import Tuple, Union

from pygeoapi import l10n
from pygeoapi.api import (
    APIRequest, API, SYSTEM_LOCALE, F_JSON, FORMAT_TYPES, F_HTML
)
from pygeoapi.flask_app import api_, get_response
from pygeoapi.process.base import (
    JobNotFoundError, ProcessorExecuteError, JobResultNotFoundError
)
from pygeoapi.process.manager.base import Subscriber
from pygeoapi.util import (
    json_serial, render_j2_template, JobStatus, RequestedProcessExecutionMode,
    to_json, DATETIME_FORMAT)
from pygeoapi_prefect.schemas import (
    RequestedProcessExecutionMode,
)
from pygeoapi_prefect.process.base import ScheduleNotFoundError
from pygeoapi_prefect.manager import _get_prefect_deployment
from flask import send_from_directory, Response, Request, g, request as flask_request
import anyio

try:
    from ..base import store_offline_token, revoke_and_delete_offline_token, has_offline_token
except ImportError:
    from process.base import store_offline_token, revoke_and_delete_offline_token, has_offline_token

# Header the frontend may use to supply the user's offline refresh token when creating a
# schedule (obtained via an offline_access login). A body field is also accepted as a fallback.
OFFLINE_TOKEN_HEADER = "X-KM-Offline-Token"

# class ScheduleNotFoundError(Exception):
#     pass

logger = logging.getLogger(__name__)

if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        logger.handlers = gunicorn_logger.handlers
        logger.setLevel(gunicorn_logger.level)


def execute_from_flask_custom(api_function, request: Request, *args,
                       skip_valid_check=False) -> Response:
    """
    Executes API function from Flask

    :param api_function: API function
    :param request: request object
    :param *args: variable length additional arguments
    :param skip_validity_check: bool

    :returns: A Response instance
    """

    api_request = APIRequest.from_flask(request, api_.locales)

    content: Union[str, bytes]

    if not skip_valid_check and not api_request.is_valid():
        headers, status, content = api_.get_format_exception(api_request)
    else:
        result = api_function(api_, api_request, *args)
        if isinstance(result, Response):
            return result
        headers, status, content = result
        content = apply_gzip(headers, content)

    return get_response((headers, status, content))



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

    # The user's offline refresh token is needed so scheduled runs can access the Data
    # Management API on behalf of the user under Standard Token Exchange (v2). It is supplied
    # by the frontend either via a header or in the request body under "properties".
    offline_token = flask_request.headers.get(OFFLINE_TOKEN_HEADER) \
        or data.get('properties', {}).get('offline_token')

    try:
        logger.debug('Scheduling process')

        result = api.manager.schedule_process(
            process_id, data_dict)

        schedule_id, mime_type, status = result

        if status not in (JobStatus.failed,):
            if offline_token:
                try:
                    store_offline_token(schedule_id, offline_token)
                    logger.info(f"Stored offline token for schedule {schedule_id}")
                except Exception as err:
                    logger.error(f"Failed to store offline token for schedule {schedule_id}: {err}")
            else:
                logger.warning(
                    f"No offline token supplied for schedule {schedule_id}; scheduled runs "
                    f"will fail to authenticate against the Data Management API. Provide it via "
                    f"the '{OFFLINE_TOKEN_HEADER}' header or a 'properties.offline_token' body field."
                )

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


def set_offline_token(api: API, request: APIRequest, schedule_id) -> Tuple[dict, int, str]:
    """
    Attach (or replace) the offline token of an existing schedule.

    This re-authorizes a schedule - notably schedules created by a previous version that used
    Token Exchange v1 and therefore have no stored offline token - without recreating it, so its
    id, cron and run history are preserved. The caller must be the owner of the schedule.

    :param request: A request object
    :param schedule_id: id of the schedule to re-authorize

    :returns: tuple of headers, status code, content
    """
    headers = request.get_response_headers(SYSTEM_LOCALE, **api.api_headers)

    # 1. Verify the schedule exists and fetch its owner (stored user_id) from the deployment.
    deploy_name = api.manager._schedule_id_to_deploy_name(schedule_id)
    try:
        deploy_details = anyio.run(_get_prefect_deployment, deploy_name)
    except Exception as err:
        logger.error(f"Could not fetch deployment for schedule {schedule_id}: {err}")
        deploy_details = None
    if not deploy_details:
        return api.get_exception(
            HTTPStatus.NOT_FOUND, headers, request.format, 'NoSuchSchedule', schedule_id)

    deployment = deploy_details[0]
    try:
        owner_id = deployment.parameters['execution_request']['properties']['user_id']
    except (KeyError, TypeError):
        owner_id = None

    # 2. Ownership check: only the user who created the schedule may re-authorize it.
    current_user_id = g.get('user_id')
    if owner_id and current_user_id and owner_id != current_user_id:
        return api.get_exception(
            HTTPStatus.FORBIDDEN, headers, request.format,
            'Forbidden', 'You are not the owner of this schedule.')

    # 3. Read the offline token from the header or the request body.
    offline_token = flask_request.headers.get(OFFLINE_TOKEN_HEADER)
    if not offline_token:
        try:
            body = json.loads(request.data.decode()) if request.data else {}
        except (json.decoder.JSONDecodeError, TypeError, AttributeError, UnicodeDecodeError):
            body = {}
        offline_token = body.get('offline_token') \
            or body.get('properties', {}).get('offline_token')
    if not offline_token:
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format, 'MissingParameterValue',
            f"Missing offline token. Provide it via the '{OFFLINE_TOKEN_HEADER}' header or an "
            f"'offline_token' body field.")

    # 4. Store the offline token for this schedule.
    try:
        store_offline_token(schedule_id, offline_token)
    except Exception as err:
        logger.error(f"Failed to store offline token for schedule {schedule_id}: {err}")
        return api.get_exception(
            HTTPStatus.INTERNAL_SERVER_ERROR, headers, request.format, 'InternalError', schedule_id)

    logger.info(f"Stored offline token for schedule {schedule_id} (re-authorization)")
    response = {
        'scheduleID': schedule_id,
        'status': 'AUTHORIZED',
        'message': 'Offline token stored for schedule'
    }
    return headers, HTTPStatus.OK, to_json(response, api.pretty_print)


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
        except ScheduleNotFoundError:
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
        logger.debug("schedule data model:")
        logger.debug(schedule_)
        schedule2 = {
            'type': 'process',
            'processID': schedule_['process_id'],
            'scheduleID': schedule_['schedule_id'],
            'jobIDs': schedule_['job_ids'],
            'status': schedule_['status'],
            'scheduleCreated': schedule_['created'],
            'scheduleUpdated': schedule_['updated'],
            'scheduleActive': schedule_['active'],
            'scheduleCron': schedule_['cron'],
            'inputs': schedule_['inputs'] if 'inputs' in schedule_ else '',
            # False for legacy (v1) schedules that still need to be re-authorized with an
            # offline token before their scheduled runs can access the Data Management API.
            'offlineTokenRegistered': has_offline_token(schedule_['schedule_id'])
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


def delete_schedule(api: API, request: APIRequest, schedule_id) -> Tuple[dict, int, str]:
    """
    Delete a schedule

    :param schedule_id: schedule identifier

    :returns: tuple of headers, status code, content
    """

    response_headers = request.get_response_headers(
        SYSTEM_LOCALE, **api.api_headers)
    try:
        success = api.manager.delete_schedule(schedule_id)
    except ScheduleNotFoundError:
        return api.get_exception(
            HTTPStatus.NOT_FOUND, response_headers, request.format,
            'NoSuchSchedule', schedule_id
        )
    else:
        if success:
            # Revoke the stored offline token at Keycloak and remove its Secret block so no
            # long-lived user credential lingers after the schedule is gone.
            try:
                revoke_and_delete_offline_token(schedule_id, logger)
            except Exception as err:
                logger.warning(f"Failed to revoke offline token for schedule {schedule_id}: {err}")

            http_status = HTTPStatus.OK
            schedules_url = f"{api.base_url}/schedules"

            response = {
                'scheduleID': schedule_id,
                'status': "DISMISSED",
                'message': 'Schedule dismissed',
                'links': [{
                    'href': schedules_url,
                    'rel': 'up',
                    'type': FORMAT_TYPES[F_JSON],
                    'title': l10n.translate('The schedule list for the current process', request.locale)  # noqa
                }]
            }
        else:
            return api.get_exception(
                HTTPStatus.INTERNAL_SERVER_ERROR, response_headers,
                request.format, 'InternalError', schedule_id
            )
    logger.info(response)
    # TODO: this response does not have any headers
    return {}, http_status, to_json(response, api.pretty_print)

def execute_schedule(api: API, request: APIRequest, schedule_id) -> Tuple[dict, int, str]:
    """
    Trigger a schedule execution

    :param schedule_id: schedule identifier

    :returns: tuple of headers, status code, content
    """

    response_headers = request.get_response_headers(
        SYSTEM_LOCALE, **api.api_headers)
    try:
        job_id = api.manager.trigger_flow_from_schedule(schedule_id)
    except ScheduleNotFoundError:
        return api.get_exception(
            HTTPStatus.NOT_FOUND, response_headers, request.format,
            'NoSuchSchedule', schedule_id
        )
    else:
        if job_id is not None:
            http_status = HTTPStatus.OK
            schedules_url = f"{api.base_url}/schedules"

            response = {
                'scheduleID': schedule_id,
                'jobID': job_id,
                'status': "CREATED",
                'message': 'Schedule execution triggered',
                'links': [{
                    'href': schedules_url,
                    'rel': 'up',
                    'type': FORMAT_TYPES[F_JSON],
                    'title': l10n.translate('The schedule list for the current process', request.locale)  # noqa
                }]
            }
        else:
            return api.get_exception(
                HTTPStatus.INTERNAL_SERVER_ERROR, response_headers,
                request.format, 'InternalError', schedule_id
            )
    logger.info(response)
    # TODO: this response does not have any headers
    return {}, http_status, to_json(response, api.pretty_print)


def download_file(api: API, request: APIRequest, job_id, resultdir):
    headers = request.get_response_headers(SYSTEM_LOCALE,
                                           **api.api_headers)
    try:
        job = api.manager.get_job(job_id)
    except JobNotFoundError:
        return api.get_exception(
            HTTPStatus.NOT_FOUND, headers,
            request.format, 'NoSuchJob', job_id
        )

    status = JobStatus[job['status']]

    if status == JobStatus.running:
        msg = 'job still running'
        return api.get_exception(
            HTTPStatus.NOT_FOUND, headers,
            request.format, 'ResultNotReady', msg)

    elif status == JobStatus.accepted:
        # NOTE: this case is not mentioned in the specification
        msg = 'job accepted but not yet running'
        return api.get_exception(
            HTTPStatus.NOT_FOUND, headers,
            request.format, 'ResultNotReady', msg)

    elif status == JobStatus.failed:
        msg = 'job failed'
        return api.get_exception(
            HTTPStatus.BAD_REQUEST, headers, request.format,
            'InvalidParameterValue', msg)

    try:
        mimetype, job_output = api.manager.get_job_result(job_id)
        output = json.loads(job_output.decode('utf-8'))
        file_name = output["file"]["title"]
        # If output has a userId we have to check if requesting user is allowed to fetch export results
        if "userId" in output:
            result_user_id =  output["userId"]
            try:
                current_user_id = g.get("user_id")
                if result_user_id != current_user_id:
                    return api.get_exception(
                        HTTPStatus.FORBIDDEN, headers,
                        request.format, 'JobResultNotFoundError', job_id
                    )
            except AttributeError as err:
                logger.warning(err)
    except JobResultNotFoundError:
        return api.get_exception(
            HTTPStatus.INTERNAL_SERVER_ERROR, headers,
            request.format, 'JobResultNotFound', job_id
        )
    filedir = os.path.join(resultdir, os.path.dirname(file_name))
    file = os.path.basename(file_name)
    logger.info(f"Export file {file} from {filedir}")
    return send_from_directory(
        directory=filedir,
        path=file,
        as_attachment=True,
        mimetype='application/octet-stream'
    )

