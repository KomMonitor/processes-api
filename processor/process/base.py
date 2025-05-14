import abc
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from logging import Logger
import urllib.parse as urlparse
import json

import openapi_client
import prefect

import requests
from openapi_client import ApiClient, ApiException
from prefect import task, flow, get_run_logger
from pygeoapi.util import JobStatus

from auth import KC_CLIENT_ID, KC_CLIENT_SECRET, KC_HOSTNAME, KC_HOSTNAME_PATH, KC_REALM_NAME
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType, ProcessIOFormat, ProcessOutput, \
    ExecutionQualifiedInputValue, ExecutionInputValueNoObject, ExecutionInputValueNoObjectArray
from pygeoapi_prefect.utils import get_storage
import pyinstrument

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
        if type(v) is ExecutionInputValueNoObject or type(v) is ExecutionInputValueNoObjectArray:
            inputs[k] = v.model_dump()
        elif type(v) is ExecutionQualifiedInputValue:
            inputs[k] = v.model_dump()["value"]
        else:
            raise Exception("Unsupported input value!")
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
    filename = f"result-{job_id}.json"
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


class ExecutionErrorType(str, Enum):
    MISSING_TIMESTAMP = "MISSING_TIMESTAMP"
    MISSING_DATASET = "MISSING_DATASET"
    MISSING_SPATIAL_UNIT = "MISSING_SPATIAL_UNIT"
    MISSING_SPATIAL_UNIT_FEATURE = "MISSING_SPATIAL_UNIT_FEATURE"
    DATAMANAGEMENT_API_ERROR = "DATAMANAGEMENT_API_ERROR"
    PROCESSING_ERROR = "PROCESSING_ERROR"


class ExecutionMode(str, Enum):
    MISSING = "MISSING"
    ALL = "ALL"
    DATES = "DATES"


class ExecutionResourceType(str, Enum):
    GEORESOURCE = "GEORESOURCE"
    INDICATOR = "INDICATOR"


class KommonitorResult:
    def __init__(self):
        self._values = []
        self._su_result = None

    @property
    def values(self):
        return self._values

    def init_spatial_unit_result(self, spatial_unit_id: str, spatial_unit_controller: openapi_client.SpatialUnitsControllerApi):
         # query 'spatialUnitLevel' in order to prepare the indicator PUT-body
         su_meta = spatial_unit_controller.get_spatial_units_by_id(spatial_unit_id)

         self._su_result = {
             "applicableSpatialUnit": su_meta.spatial_unit_level
         }

    def complete_spatial_unit_result(self):
        if self._su_result:
            self._values.append(self._su_result)
        self._su_result = None

    def add_indicator_values(self, values: list):
        self._su_result["indicatorValues"] = values


class KommonitorJobSummary:
    def __init__(self):
        self._summary = []
        self._su_summary = None

    @property
    def summary(self):
        return self._summary

    def init_spatial_unit_summary(self, spatial_unit_id: str):
         self._su_summary = {
             "spatialUnitId": spatial_unit_id,
             "modifiedResource": None,
             "numberOfIntegratedIndicatorFeatures": None,
             "integratedTargetDates": [],
             "errorsOccurred": []
         }

    def complete_spatial_unit_summary(self):
        if self._su_summary:
            self._summary.append(self._su_summary)
        self._su_summary = None

    def add_modified_resource(self, base_url: str, indicator_id: str, spatial_unit_id: str):
        self._su_summary["modifiedResource"] = urlparse.urljoin(base_url, f"indicators/{indicator_id}/{spatial_unit_id}")

    def add_number_of_integrated_features(self, number: int):
        self._su_summary["numberOfIntegratedIndicatorFeatures"] = number

    def add_integrated_target_dates(self, dates: list):
        self._su_summary["integratedTargetDates"] = dates

    def add_missing_timestamp_error(self, resource_type: str, dataset_id: str, timestamps: list):
        self._su_summary["errorsOccurred"].append(
            {
                "type": "missingTimestamp",
                "affectedResourceType": resource_type,
                "affectedDatasetId": dataset_id,
                "affectedTimestamps": timestamps,
                "affectedSpatialUnitFeatures": [],
                "errorMessage": f"Timestamps are missing for {resource_type} with ID {dataset_id}."
            }
        )

    def add_missing_dataset_error(self, resource_type: str, dataset_id: str):
        self._su_summary["errorsOccurred"].append(
            {
                "type": "missingDataset",
                "affectedResourceType": resource_type,
                "affectedDatasetId": dataset_id,
                "affectedTimestamps": [],
                "affectedSpatialUnitFeatures": [],
                "errorMessage": f"The {resource_type} with ID {dataset_id} is missing."
            }
        )

    def add_missing_spatial_unit_error(self, dataset_id: str):
        su_id = self._su_summary["spatialUnitId"]
        self._su_summary["errorsOccurred"].append(
            {
                "type": "missingSpatialUnit",
                "affectedResourceType": "indicator",
                "affectedDatasetId": dataset_id,
                "affectedTimestamps": [],
                "affectedSpatialUnitFeatures": [],
                "errorMessage": f"The spatial unit {su_id} is missing for indicator {dataset_id}."
            }
        )

    def add_missing_spatial_unit_feature_error(self, dataset_id: str, features: list):
        self._su_summary["errorsOccurred"].append(
            {
                "type": "missingSpatialUnitFeature",
                "affectedResourceType": "indicator",
                "affectedDatasetId": dataset_id,
                "affectedTimestamps": [],
                "affectedSpatialUnitFeatures": features,
                "errorMessage": f"Spatial unit features are missing for indicator {dataset_id}."
            }
        )

    def add_data_management_api_error(self, resource_type: str, dataset_id: str, error_code: int, error_message: str, spatial_unit_id: str = None):
        if spatial_unit_id:
            for su_summary in self._summary:
                if su_summary["spatialUnitId"] == spatial_unit_id:
                    su_summary["errorsOccurred"].append(
                        {
                            "type": "dataManagementApiError",
                            "affectedResourceType": resource_type,
                            "affectedDatasetId": dataset_id,
                            "affectedTimestamps": [],
                            "affectedSpatialUnitFeatures": [],
                            "dataManagementApiErrorCode": error_code,
                            "errorMessage": f"Error while calling API for {resource_type} with ID {dataset_id}: {error_message}."
                        }
                    )
        else:
            self._su_summary["errorsOccurred"].append(
                {
                    "type": "dataManagementApiError",
                    "affectedResourceType": resource_type,
                    "affectedDatasetId": dataset_id,
                    "affectedTimestamps": [],
                    "affectedSpatialUnitFeatures": [],
                    "dataManagementApiErrorCode": error_code,
                    "errorMessage": f"Error while calling API for {resource_type} with ID {dataset_id}: {error_message}."
                }
        )

    def add_processing_error(self, resource_type: str, dataset_id: str, error_message: str):
        self._su_summary["errorsOccurred"].append(
            {
                "type": "processingError",
                "affectedResourceType": resource_type,
                "affectedDatasetId": dataset_id,
                "affectedTimestamps": [],
                "affectedSpatialUnitFeatures": [],
                "errorMessage": f"Error while processing {resource_type} with ID {dataset_id}: {error_message}."
            }
        )

    def mark_failed_job(self, spatial_unit_id: str):
        for su_summary in self._summary:
            if su_summary["spatialUnitId"] == spatial_unit_id:
                su_summary["modifiedResource"] = None,
                su_summary["numberOfIntegratedIndicatorFeatures"] = None
                su_summary["integratedTargetDates"] = []


def fetch_indicator_timeseries(controller: openapi_client.IndicatorsControllerApi, indicator_id: str,
                               spatial_unit_id: str, job_summary: KommonitorJobSummary, logger: logging.Logger):
    try:
        su_metadata = controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(indicator_id, spatial_unit_id)
        return su_metadata
    except ApiException as e:
        logger.error(f"Exception when fetching Indicator timeseries data from DataManagementAPI: {e}")
        job_summary.add_data_management_api_error("indicator", indicator_id, e.status, e.data)
        return None


def fetch_spatial_unit_metadata(controller: openapi_client.SpatialUnitsControllerApi, spatial_unit_id: str,
                                job_summary: KommonitorJobSummary, logger: logging.Logger):
    try:
        su_metadata = controller.get_spatial_units_by_id(spatial_unit_id)
        return su_metadata
    except ApiException as e:
        logger.error(f"Exception when fetching Spatial Unit metadata from DataManagementAPI: {e}")
        job_summary.add_data_management_api_error("spatial unit", spatial_unit_id, e.status, e.data)
        return None


class KommonitorProcess(BasePrefectProcessor):
    result_storage_block = None

    common_inputs = {
        "target_indicator_id": ProcessInput(
            title="target_indicator_id",
            schema_=ProcessIOSchema(
                type_=ProcessIOType.STRING
            )
        ),
        "target_spatial_units": ProcessInput(
            title="target_spatial_units",
            schema_=ProcessIOSchema(
                type_=ProcessIOType.ARRAY,
                items=ProcessIOSchema(type_=ProcessIOType.STRING),
                min_items=1
            )
        ),
        "target_time ": ProcessInput(
            title="target_time",
            schema_=ProcessIOSchema(
                type_=ProcessIOType.OBJECT,
                required=["mode"],
                properties={
                    "mode": ProcessIOSchema(type_=ProcessIOType.STRING, enum=[ExecutionMode.MISSING, ExecutionMode.ALL, ExecutionMode.DATES]),
                    "includeDates": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)),
                    "excludeDates": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING))
                },
                default={
                    "mode": ExecutionMode.MISSING,
                    "includeDates": [],
                    "excludeDates": []
                }
            )
        ),
        "execution_interval ": ProcessInput(
            title="execution_interval",
            schema_=ProcessIOSchema(
                type_=ProcessIOType.OBJECT,
                required=["cron"],
                properties={
                    "cron": ProcessIOSchema(type_=ProcessIOType.STRING)
                },
                default={
                    "cron": "0 0 1 * *"
                }
            ),
        )
    }

    error_type =  ProcessIOSchema(
        type_=ProcessIOType.ARRAY,
        items=ProcessIOSchema(
            type_=ProcessIOType.OBJECT,
            required=["type", "affectedResourceType", "affectedDatasetId", "affectedTimestamps", "affectedSpatialUnitFeatures", "errorMessage"],
            properties={
                "type": ProcessIOSchema(type_=ProcessIOType.STRING, enum=[ExecutionErrorType.MISSING_TIMESTAMP, ExecutionErrorType.MISSING_DATASET, ExecutionErrorType.MISSING_SPATIAL_UNIT, ExecutionErrorType.MISSING_SPATIAL_UNIT_FEATURE, ExecutionErrorType.DATAMANAGEMENT_API_ERROR, ExecutionErrorType.PROCESSING_ERROR]),
                "affectedResourceType": ProcessIOSchema(type_=ProcessIOType.STRING, enum=[ExecutionResourceType.INDICATOR, ExecutionResourceType.GEORESOURCE]),
                "affectedDatasetId": ProcessIOSchema(type_=ProcessIOType.STRING, format_=ProcessIOFormat.UUID),
                "affectedTimestamps": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING, format_=ProcessIOFormat.DATE)),
                "affectedSpatialUnitFeatures": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)),
                "errorMessage": ProcessIOSchema(type_=ProcessIOType.STRING)
            }
        )
    )

    indicator_value_type = ProcessIOSchema(
        type_=ProcessIOType.OBJECT,
        required=["spatialReferenceKey", "valueMapping"],
        properties={
            "spatialReferenceKey": ProcessIOSchema(type_=ProcessIOType.STRING),
            "valueMapping": ProcessIOSchema(
                type_=ProcessIOType.ARRAY,
                items=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    required=["indicatorValue", "timestamp"],
                    properties={
                        "indicatorValue": ProcessIOSchema(type_=ProcessIOType.NUMBER),
                        "timestamp": ProcessIOSchema(type_=ProcessIOType.STRING, format_=ProcessIOFormat.DATE)
                    }
                )
            )
        }
    )

    common_output = {
        "jobSummary": ProcessOutput(
            schema_=ProcessIOSchema(
                type_=ProcessIOType.ARRAY,
                items=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    properties={
                        "spatialUnitId": ProcessIOSchema(type_=ProcessIOType.STRING),
                        "modifiedResource": ProcessIOSchema(type_=ProcessIOType.STRING, format_=ProcessIOFormat.URI),
                        "numberOfIntegratedIndicatorFeatures": ProcessIOSchema(type_=ProcessIOType.INTEGER),
                        "integratedTargetDates": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING, format_=ProcessIOFormat.DATE)),
                        "errorsOccurred": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=error_type)
                    }
                ),
                content_media_type= "application/json"
            )
        ),
        "resultData": ProcessOutput(
            schema_=ProcessIOSchema(
                type_=ProcessIOType.ARRAY,
                items=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    required=["applicableSpatialUnit", "indicatorValues"],
                    properties={
                        "applicableSpatialUnit": ProcessIOSchema(type_=ProcessIOType.STRING),
                        "indicatorValues": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=indicator_value_type),
                    }
                ),
                content_media_type="application/json"
            )
        )
    }


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
        status, result, job_summary = p.run(config, logger, dmc)
        print(status)
        if status == JobStatus.failed:
            output = {
                "jobSummary": job_summary.summary,
                "resultData": [],
            }
            return store_output_as_file(job_id, output)
        else:
            output = {
                "jobSummary": None,
                "resultData": []
            }
            indicator_id = inputs["target_indicator_id"]
            for res in result.values:
                indicators_controller = openapi_client.IndicatorsControllerApi(dmc)
                res["allowedRoles"] = []
                print(res)
                try:
                    resp = indicators_controller.update_indicator_as_body_with_http_info(
                        indicator_id=indicator_id,
                        indicator_data=res
                    )
                    if resp.status_code == 200:
                        output["resultData"].append(res)
                    else:
                        job_summary.mark_failed_job(res["applicableSpatialUnit"])
                except ApiException as e:
                    logger.error(f"Exception when calling DataManagementAPI: {e}")
                    job_summary.add_data_management_api_error("indicator", indicator_id, e.status, e.reason, res["applicableSpatialUnit"])
                    job_summary.mark_failed_job(res["applicableSpatialUnit"])
            output["jobSummary"] = job_summary.summary
            return store_output_as_file(job_id, output)

    @abc.abstractmethod
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            dmc: ApiClient) -> (JobStatus, KommonitorResult, KommonitorJobSummary):
        ...

    @property
    def process_description(self) -> schemas.ProcessDescription:
        description = self.detailed_process_description
        return description

    @property
    @abc.abstractmethod
    def detailed_process_description(self) -> schemas.ProcessDescription:
        ...

