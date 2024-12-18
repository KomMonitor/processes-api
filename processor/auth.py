import os
import time

import requests
from authlib.oauth2.rfc6750 import InvalidTokenError
from authlib.oauth2.rfc7662 import IntrospectTokenValidator, IntrospectionToken
from flask import g
from oauthlib.oauth2 import OAuth2Token

KC_CLIENT_ID = os.getenv('KC_CLIENT_ID', "kommonitor-processor")
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET', "nichJZ3Sfqz094AGRYeYP1hlv3LWRvCc")
KC_HOSTNAME = os.getenv('KC_HOSTNAME', "demo.kommonitor.de.52north.org")
KC_REALM_NAME = os.getenv('KC_REALM_NAME', "kommonitor-demo")
KC_HOSTNAME_PATH = os.getenv('KC_HOSTNAME_PATH', "/keycloak")


class MyIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = f"https://{KC_HOSTNAME}{KC_HOSTNAME_PATH}/realms/{KC_REALM_NAME}/protocol/openid-connect/token/introspect"
        data = {'token': token_string[7:], 'token_type_hint': 'access_token'}
        auth = (KC_CLIENT_ID, KC_CLIENT_SECRET)
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        token = resp.json()
        # Store username and roles in context
        if token["active"]:
            g.user = token["username"]
            g.roles = token["realm_access"]["roles"]
            g.token = resp.content
        else:
            g.user = None
            g.roles = None

        return token

    def validate_token(self, token, scopes, request):
        if not token or not token["active"] or token["exp"] < time.time():
            raise InvalidTokenError()

        # require kommonitor-admin for now
        if "kommonitor-creator" not in token["realm_access"]["roles"]:
            print("access denied - missing required roles!")
            raise InvalidTokenError()
