import json
from typing import Tuple
import logging
import math

import openapi_client
from openapi_client import ApiClient
from prefect import task, flow
from prefect.cache_policies import NO_CACHE
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus
from pygeoapi_prefect import schemas
from pygeoapi_prefect.schemas import ProcessDescription, ProcessJobControlOption, Parameter, \
    AdditionalProcessIOParameters
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType

# from ..base import DataManagementException

try:
    from .. import pykmhelper
except ImportError:
    from processor.process import pykmhelper

try:
    from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
except ImportError:
    from processor.process.pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType

try:
    from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name
except ImportError:
    from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name


@flow(persist_result=True, name="hello_world", flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(HelloWorld.run, job_id, execution_request)

class HelloWorld(KommonitorProcess):

    process_flow = process_flow

    detailed_process_description = ProcessDescription(
        id="hello-world",
        version="1.0.0",
        title="Hello World! ",
        example={
            "name": "Peter",
        },
        additional_parameters=AdditionalProcessIOParameters(
            parameters=[
                Parameter(
                    name="legend",
                    value=["Hello World"]
                ),
                Parameter(
                    name="formula",
                    value=["log_n(very complex formula)"]
                ),
            ]
        ),
        jobControlOptions=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs={
            "name": ProcessInput(
                title="name",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
        },
        outputs = KommonitorProcess.common_output
    )

    @staticmethod
    @task(cache_policy=NO_CACHE)
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> Tuple[JobStatus, KommonitorResult, KommonitorJobSummary]:

        # 1. Load inputs
        inputs = config.inputs

        # 2. Log some useful stuff
        logger.debug("Starting execution...")

        try:
            # 3. Generate result
            result = f"Hello {inputs.get('name')}"

            # 4.1 Return success and result
            return JobStatus.successful, None

        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            logger.error(f"Exception when processing: {e}")
            return JobStatus.failed, None
