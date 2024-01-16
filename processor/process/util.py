import ast
import os
from enum import Enum
from logging import Logger
from typing import Dict

import openapi_client
import requests
from openapi_client import ApiClient
from prefect import task

from pygeoapi_prefect import schemas

class AggregationType(Enum):
    SUM = 1
    AVERAGE = 2


def as_geojson(raw_string: str) -> Dict:
    """ reads geojson """
    return ast.literal_eval(raw_string)


KOMMONITOR_DATA_MANAGEMENT_URL = os.getenv('KOMMONITOR_DATA_MANAGEMENT_URL', "keycloak:8080")
KC_CLIENT_ID = os.getenv('KC_CLIENT_ID', "kommonitor-processor")
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET', "secret")


@task
def data_management_client(logger: Logger, execute_request: schemas.ExecuteRequest, private: bool = False) -> ApiClient:
    # TODO: check how this can be encapsulated and made intransparent from the user
    # Maybe migrate into manager?

    if private:
        payload = {
            "client_id": KC_CLIENT_ID,
            "client_secret": KC_CLIENT_SECRET,
            "grant_type": "password",
            "username": "test",
            "password": "test",
            "Content-Type": "application/x-www-form-urlencoded",
            "requested_roles": execute_request.properties.get("roles", "")
        }

        logger.info(f"Requesting token with roles: {execute_request.properties.get('roles', '')}")
        http = "http://keycloak:8080/realms/kommonitor/protocol/openid-connect/token"
        a = requests.post(http, data=payload)
        a = a.json()

        token = a['access_token']
        configuration = openapi_client.Configuration(
            host=KOMMONITOR_DATA_MANAGEMENT_URL,
            access_token=token
        )
        return openapi_client.ApiClient(configuration)
    else:
        logger.debug(f"Using Public API without token")
        configuration = openapi_client.Configuration(
            host=KOMMONITOR_DATA_MANAGEMENT_URL
        )
        return openapi_client.ApiClient(configuration)
