import abc
import datetime as dt
import logging
import os
from dataclasses import dataclass
from logging import Logger
from typing import Dict, Union, Optional

import openapi_client
import prefect
from prefect.filesystems import LocalFileSystem
from prefect.serializers import JSONSerializer
import requests
from flask import g
from openapi_client import ApiClient
from prefect import task, flow, get_run_logger
from pygeoapi.util import JobStatus

from processor.auth import KC_CLIENT_ID, KC_CLIENT_SECRET, KC_HOSTNAME, KC_HOSTNAME_PATH, KC_REALM_NAME
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.schemas import JobStatusInfoInternal, OutputExecutionResultInternal


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


class KommonitorProcess(BasePrefectProcessor):
    result_storage_block = None
    process_flow = flow

    @staticmethod
    @task
    def format_inputs(execution_request: schemas.ExecuteRequest):
        inputs = {}

        for k, v in execution_request.inputs.items():
            inputs[k] = v.root
        return inputs

    @staticmethod
    @task
    def setup_logging(job_id: str) -> Logger:
        os.mkdir(f"{PROCESS_RESULTS_DIR}/{job_id}/")
        log_path = f"{PROCESS_RESULTS_DIR}/{job_id}/log.txt"
        filelogger = logging.FileHandler(log_path)
        filelogger.setLevel(logging.DEBUG)
        logger = get_run_logger()
        logger.logger.addHandler(filelogger)
        logger.debug("Setup logging ...")
        return logger

    @staticmethod
    @task
    def store_output(job_id: str, output: dict) -> str:
        storage = LocalFileSystem()
        serializer = JSONSerializer()
        result_path = f"{PROCESS_RESULTS_DIR}/{job_id}/result.json"
        result = serializer.dumps(output)
        storage.write_path(result_path, result)
        return result_path

    @staticmethod
    @flow(persist_result=True)
    def process_flow(
            processor,
            job_id: str,
            result_storage_block: str | None,
            process_description: schemas.ProcessDescription,
            execution_request: schemas.ExecuteRequest
    ) -> Union[schemas.JobStatusInfoInternal, prefect.states.State]:
        print(processor)

        ## Setup
        logger = KommonitorProcess.setup_logging(job_id)
        inputs = KommonitorProcess.format_inputs(execution_request)

        config = KommonitorProcessConfig(job_id, inputs, f"{job_id}/output-result.txt")
        dmc = data_management_client(logger, execution_request, True)

        ## Run process
        status, outputs = processor.run(config, logger, dmc)

        res_path = KommonitorProcess.store_output(job_id, outputs)

        ## Reformat output
        return JobStatusInfoInternal(
            jobID=job_id,
            processID=process_description.id,
            status=status,
            updated=dt.datetime.now(),
            generated_outputs={
                "result": schemas.OutputExecutionResultInternal(
                    location=res_path,
                    media_type=(
                        process_description.outputs["result"].schema_.content_media_type
                    ),
                )
            },
        )

    @staticmethod
    @abc.abstractmethod
    def run(config: KommonitorProcessConfig,
            logger: logging.Logger,
            dmc: ApiClient) -> (JobStatus, Optional[Dict[str, OutputExecutionResultInternal]]):
        ...

    @property
    @abc.abstractmethod
    def process_description(self) -> schemas.ProcessDescription:
        ...
