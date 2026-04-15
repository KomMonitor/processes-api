import logging
import openapi_client
import json
import os
import abc
import geopandas as gpd
from openapi_client import ApiClient, ApiException
from prefect import task, get_run_logger, Task, runtime, flow
from prefect.cache_policies import NO_CACHE
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType, ProcessDescription, ProcessJobControlOption, AdditionalProcessIOParameters, Parameter

from .base import KommonitorProcessConfig, setup_logging, format_inputs, data_management_client, store_output_as_file, close_logging

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
        config = KommonitorProcessConfig(flow_id, inputs, f"{flow_id}/output-result.txt")
        dmc = data_management_client(logger, execution_request, True)

        ## Run process
        output = run(config=config, logger=logger, data_management_client=dmc, job_id=job_id, flow_id=flow_id)
        output["userId"] = execution_request.properties["user_id"]
        logger.debug(output)
        result = store_output_as_file(flow_id, output, logger)
        close_logging(logger, handler)
        return result

    @staticmethod
    @task(cache_policy=NO_CACHE)
    @abc.abstractmethod
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            dmc: ApiClient,
            job_id: str,
            flow_id: str) -> dict:
        ...
