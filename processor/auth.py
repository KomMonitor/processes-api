import os
import time

import requests
from authlib.oauth2.rfc6750 import InvalidTokenError
from authlib.oauth2.rfc7662 import IntrospectTokenValidator, IntrospectionToken
from flask import g
from oauthlib.oauth2 import OAuth2Token

KC_URL = os.getenv('KC_URL', "https://keycloak:8443")
KC_CLIENT_ID = os.getenv('KC_CLIENT_ID', "kommonitor-processor")
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET', "processor-secret")
KC_REALM_NAME = os.getenv('KC_REALM_NAME', "kommonitor-demo")
ALLOWED_ROLES = tuple(os.getenv('ALLOWED_ROLES', "kommonitor-creator").split(","))


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
        if not token or not token["active"] or token["exp"] < time.time():
            raise InvalidTokenError()

        if not any(role.endswith(ALLOWED_ROLES) for role in token["realm_access"]["roles"]):
            print("access denied - missing required roles!")
            raise InvalidTokenError()
