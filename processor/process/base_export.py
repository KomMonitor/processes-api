import abc
import logging
import os
import shutil

from openapi_client import ApiClient
from prefect import task, Task, runtime
from prefect.cache_policies import NO_CACHE
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor

from .base import KommonitorProcessConfig, setup_logging, format_inputs, data_management_client, store_output_as_file, \
    close_logging, PROCESSES_API_URL

PROCESS_RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', "/tmp")

def create_response(server_url: str, job_id: str, flow_id: str) -> dict:
    return {
        "status": "successful",
        "file": {
            "href": f"{server_url}/exports/{job_id}",
            "rel": "enclosure",
            "type": "application/octet-stream",
            "title": f"{flow_id}/export_data.zip"
        }}

class ExportProcess(BasePrefectProcessor):
    def __init__(self, processor_def: dict):
        super().__init__(processor_def)

    @property
    def process_description(self) -> schemas.ProcessDescription:
        description = self.detailed_process_description
        return description

    @property
    @abc.abstractmethod
    def detailed_process_description(self) -> schemas.ProcessDescription:
        ...

    @staticmethod
    def execute_process_flow(
            run: Task,
            job_id: str,
            execution_request: schemas.ExecuteRequest
    ) -> dict:
        ## Setup
        flow_id = runtime.flow_run.name
        logger, handler = setup_logging(flow_id)
        logger.info(f"Flow run name: {flow_id}")

        inputs = format_inputs(execution_request)
        config = KommonitorProcessConfig(flow_id, inputs, f"{flow_id}/output-result.txt", PROCESSES_API_URL)

        export_dir = os.path.join(PROCESS_RESULTS_DIR, flow_id, "export_data")
        if not os.path.isdir(export_dir):
            os.mkdir(export_dir)

        if "user_id" in execution_request.properties:
            dmc = data_management_client(logger, execution_request, True)
            run(config=config, logger=logger, data_management_client=dmc, export_dir=export_dir)
            output = create_response(config.server_url, job_id, flow_id)
            output["userId"] = execution_request.properties["user_id"]
        else:
            dmc = data_management_client(logger, execution_request, False)
            run(config=config, logger=logger, data_management_client=dmc, export_dir=export_dir)
            output = create_response(config.server_url, job_id, flow_id)
        logger.debug(output)
        shutil.make_archive(export_dir, "zip", export_dir)
        shutil.rmtree(export_dir)
        result = store_output_as_file(flow_id, output, logger)
        close_logging(logger, handler)
        return result

    @staticmethod
    @task(cache_policy=NO_CACHE)
    @abc.abstractmethod
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            dmc: ApiClient,) -> dict[str, str] | None:
        ...
