from typing import Dict, Optional

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
# from pandas import isnull
import pandas as pd

from pygeoapi.process.base import *
from pygeoapi.util import JobStatus
from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput

from ..base import KommonitorProcess, KommonitorProcessConfig
from ..util import dataio


class PercentageShare(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="percentage-share",
        version="0.0.1",
        title="Percentage share of an indicator to a reference indicator in a given spatial unit",
        example={
            "target_indicator_id": "cccca04-cc57-48d3-a801-d6b4b00fcccc",
            "target_spatial_units": ["bbbba04-cc57-48d3-a801-d6b4b00fbbbb"],
            "target_time": {
              "mode": "MISSING",
              "includeDates": [],
              "excludeDates": []
            },
            "execution_interval": {
                "cron": "0 0 1 * *"
            },
            "reference_indicator_id": "aaaaa04-cc57-48d3-a801-d6b4b00faaaa"
        },
        additional_parameters=AdditionalProcessIOParameters(
            parameters=[
                Parameter(
                    name="legend",
                    value=["Percentage share of an indicator to a reference indicator in a given spatial unit"]
                ),
                Parameter(
                    name="formula",
                    value=["(indicator_count / reference_indicator_count) * 100"]
                ),
            ]
        ),
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs=KommonitorProcess.common_inputs | {
            "reference_indicator_id": ProcessInput(
                title="reference_indicator_id",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            )
        },
        outputs = KommonitorProcess.common_output
    )

    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> (JobStatus, Dict):

        # 1. Load inputs
        inputs = config.inputs
        logger.debug("Starting execution...")

        try:
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            indicator = {}
            target_indicator_id = inputs["target_indicator_id"]
            reference_indicator_id = inputs["reference_indicator_id"]
            target_spatial_units = inputs["target_spatial_units"]
            target_time = inputs["target_time"]["includeDates"][0]
            execution_interval = inputs["execution_interval"]

            target_unit_id = target_spatial_units[0]

            data = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(target_indicator_id, target_unit_id)
            ref_data = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(reference_indicator_id, target_unit_id)

            indicator_df = dataio.indicator_timeseries_to_dataframe(data)
            ref_indicator_df = dataio.indicator_timeseries_to_dataframe(ref_data)

            merged_df = indicator_df.merge(ref_indicator_df, how="left", on=["ID", "date"],
                                           suffixes=("_target", "_ref"))
            merged_df = merged_df.dropna(subset=["value_target", "value_ref"])

            merged_df["value_target"] = pd.to_numeric(merged_df["value_target"])
            merged_df["value_ref"] = pd.to_numeric(merged_df["value_ref"])

            merged_df["result"] = merged_df["value_target"] / merged_df["value_ref"] * 100

            ts_result = dataio.dataframe_to_indicator_timeseries(merged_df)

            result = {
                "jobSummary": [],
                "results": [
                    ts_result
                ]
            }

            return JobStatus.successful, result
        except ApiException as e:
            logger.error(f"Exception when calling DataManagementAPI: {e}")
            return JobStatus.failed, None
