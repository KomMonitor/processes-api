from typing import Dict, Optional

from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from processor.process.base import KommonitorProcess, KommonitorProcessConfig
from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput


class HelloWorld(KommonitorProcess):
    process_description = ProcessDescription(
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
        outputs={
            "result": ProcessOutput(
                schema=ProcessIOSchema(
                    type=ProcessIOType.STRING,
                    contentMediaType="text/plain",
                )
            )
        },
    )

    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> (JobStatus, Optional[Dict[str, OutputExecutionResultInternal]]):

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
