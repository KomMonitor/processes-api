import os
import time
import uuid
import jwt

import requests
from authlib.oauth2.rfc6750 import InvalidTokenError
from authlib.oauth2.rfc7662 import IntrospectTokenValidator, IntrospectionToken
from flask import g, request as flask_request
from oauthlib.oauth2 import OAuth2Token

KC_URL = os.getenv('KC_URL', "https://keycloak:8443")
KC_CLIENT_ID = os.getenv('KC_CLIENT_ID', "kommonitor-processor")
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET', "processor-secret")
KC_REALM_NAME = os.getenv('KC_REALM_NAME', "kommonitor-demo")
ALLOWED_ROLES = tuple(os.getenv('ALLOWED_ROLES', "kommonitor-creator").split(","))

PUBLIC_PROCESSES = ["MultipleExport", "SingleExport", "SpatialUnitExport"]

API_GET_PROCESSES = "get_processes"
API_CREATE_PROCESS = "create_process"
API_UPDATE_PROCESS = "update_process"
API_EXECUTE_PROCESS = "execute_process_jobs"
API_SCHEDULE_PROCESS = "schedule_process"
API_GET_SCHEDULES = "get_schedules"
API_SCHEDULE_EXECUTION = "schedule_execution"
API_GET_JOBS = "get_jobs"
API_GET_JOB_RESULT = "get_job_result"
API_GET_JOB_RESULT_RESOURCE = "get_job_result_resource"
API_SEND_REPORT = "send_report"
API_DOWNLOAD_FILE = "download_file"


def check_process_authentication_required(process_id):
    if process_id in PUBLIC_PROCESSES:
        return False
    else:
        return True


def check_endpoint_authentication_required(endpoint, view_args):
    if endpoint == API_DOWNLOAD_FILE:
        return False
    elif endpoint == API_EXECUTE_PROCESS:
        process_id = view_args.get('process_id')
        return check_process_authentication_required(process_id)
    else:
        return True


import os
import requests


def get_user_token_jwt_bearer_v2(user_id: str) -> str:
    """
    Holt ein User-Token via Keycloak V2 Token Exchange (RFC 8693)
    unter Verwendung des Service Accounts der processes-api.
    """
    keycloak_url = KC_URL
    realm = KC_REALM_NAME
    client_id = KC_CLIENT_ID
    client_secret = KC_CLIENT_SECRET

    token_endpoint = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"

    # --- SCHRITT A: Eigenes Service Account Token der processes-api holen ---
    sa_payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    sa_response = requests.post(token_endpoint, data=sa_payload)
    if sa_response.status_code != 200:
        print(f"[ERROR] Service Account Token konnte nicht abgerufen werden: {sa_response.text}")
        sa_response.raise_for_status()

    sa_token = sa_response.json().get("access_token")

    # --- SCHRITT B: Eigenes Token gegen das User-Token bei Keycloak V2 tauschen ---
    exchange_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "client_id": client_id,
        "client_secret": client_secret,
        "subject_token": sa_token,
        "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "requested_subject": user_id,
        "requested_token_type": "urn:ietf:params:oauth:token-type:access_token"
    }

    exchange_response = requests.post(token_endpoint, data=exchange_payload)

    if exchange_response.status_code != 200:
        print(
            f"[ERROR Keycloak V2 Exchange] Fehlgeschlagen ({exchange_response.status_code}): {exchange_response.text}")
        exchange_response.raise_for_status()

    return exchange_response.json().get("access_token")


class KomMonitorIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = f"{KC_URL}/realms/{KC_REALM_NAME}/protocol/openid-connect/token/introspect"
        data = {'token': token_string[7:], 'token_type_hint': 'access_token'}\
            if token_string.startswith('Bearer')\
            else {'token': token_string, 'token_type_hint': 'access_token'}
        auth = (KC_CLIENT_ID, KC_CLIENT_SECRET)
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        token = resp.json()
        # Store username and roles in context
        if token["active"]:
            g.user = token["username"]
            g.user_id = token["sub"]
            g.roles = token["realm_access"]["roles"]
            g.token = resp.content
        else:
            g.user = None
            g.roles = None

        return token

    def validate_token(self, token, scopes, request):
        endpoint = flask_request.endpoint
        view_args = flask_request.view_args or {}

        requires_auth = check_endpoint_authentication_required(endpoint, view_args)

        if token is None:
            if requires_auth:
                raise InvalidTokenError()
            return

        if not token or not token["active"] or token["exp"] < time.time():
            raise InvalidTokenError()

        if not any(role.endswith(ALLOWED_ROLES) for role in token["realm_access"]["roles"]):
            print("access denied - missing required roles!")
            raise InvalidTokenError()
