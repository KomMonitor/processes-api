import abc
import json
import logging
import os
from dataclasses import dataclass
from logging import Logger
from typing import Dict, Union, Optional
import json

import openapi_client
import prefect

import requests
from openapi_client import ApiClient
from prefect import task, flow, get_run_logger
from pygeoapi.util import JobStatus

from processor.auth import KC_CLIENT_ID, KC_CLIENT_SECRET, KC_HOSTNAME, KC_HOSTNAME_PATH, KC_REALM_NAME
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.utils import get_storage


@dataclass
class KommonitorProcessConfig:
    job_id: str
    inputs: dict[str, any]
    output_path: str


KC_CLIENT_ID = os.getenv('KC_CLIENT_ID', "kommonitor-processor")
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET', "processor-secret")
KC_TARGET_CLIENT_ID = os.getenv('KC_TARGET_CLIENT_ID', "kommonitor-data-management")
KC_HOSTNAME = os.getenv('KC_HOSTNAME', "keycloak:8443")
KC_REALM_NAME = os.getenv('KC_REALM_NAME', "kommonitor-demo")
KC_HOSTNAME_PATH = os.getenv('KC_HOSTNAME_PATH', "")
KOMMONITOR_DATA_MANAGEMENT_URL = os.getenv('KOMMONITOR_DATA_MANAGEMENT_URL', "http://localhost:8085/management/")
PROCESS_RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', "http://localhost:8085/management/")


@task
def data_management_client(logger: Logger, execute_request: schemas.ExecuteRequest, private: bool = False) -> ApiClient:
    if private:

        payload = {
            "client_id": KC_CLIENT_ID,
            "client_secret": KC_CLIENT_SECRET,
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "audience": KC_TARGET_CLIENT_ID,
            "Content-Type": "application/x-www-form-urlencoded",
            "requested_subject": execute_request.properties.get("user_id", "")
        }

        logger.info(f"Requesting token for user with ID: {execute_request.properties.get('user_id', '')}")

        http = f"https://{KC_HOSTNAME}{KC_HOSTNAME_PATH}/realms/{KC_REALM_NAME}/protocol/openid-connect/token"
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


@task
def format_inputs(execution_request: schemas.ExecuteRequest):
    inputs = {}

    for k, v in execution_request.inputs.items():
        inputs[k] = v.root
    return inputs


@task
def setup_logging(job_id: str) -> Logger:
    os.mkdir(f"results/{job_id}/")
    log_path = f"results/{job_id}/log.txt"

    filelogger = logging.FileHandler(log_path)
    filelogger.setLevel(logging.DEBUG)
    logger = get_run_logger()
    logger.logger.addHandler(filelogger)
    logger.debug("Setup logging ...")
    return logger


@task
def store_output_as_file(job_id: str, output: dict) -> dict:
    storage_type = "LocalFileSystem"
    basepath = f"{PROCESS_RESULTS_DIR}"
    output_dir = get_storage(storage_type, basepath=basepath)
    filename = f"percentage-share-result-{job_id}.json"
    output_dir.write_path(filename, json.dumps(output).encode('utf-8'))
    return {
        'providers': {
            'file_storage_provider': {
                'type': storage_type,
                'basepath': basepath
            }
        },
        'results': [
            {
                'provider': 'file_storage_provider',
                'mime_type': 'text/plain',
                'location': f'{output_dir.basepath}/{filename}',
                'filename': filename
            }
        ]
    }

class KommonitorProcess(BasePrefectProcessor):
    result_storage_block = None

    def __init__(self, processor_def: dict):
        super().__init__(processor_def)
        self.process_flow.__setattr__("processor", self)

    @staticmethod
    @flow(persist_result=True)
    def process_flow(
            job_id: str,
            execution_request: schemas.ExecuteRequest
    ) -> dict:
        ## Setup
        p = prefect.context.get_run_context().flow.__getattribute__("processor")
        logger = setup_logging(job_id)
        inputs = format_inputs(execution_request)
        config = KommonitorProcessConfig(job_id, inputs, f"{job_id}/output-result.txt")
        dmc = data_management_client(logger, execution_request, True)

        ## Run process
        status, outputs = p.run(config, logger, dmc)

        ## Store output and return result
        return store_output_as_file(job_id, outputs["result"])

    @abc.abstractmethod
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            dmc: ApiClient) -> (JobStatus, Dict):
        ...

    @property
    @abc.abstractmethod
    def process_description(self) -> schemas.ProcessDescription:
        ...
