from typing import Dict, Optional

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
# from pandas import isnull
import pandas as pd

from pygeoapi.process.base import *
from pygeoapi.util import JobStatus
from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput

from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorJobSummary, KommonitorResult
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
            "base_indicator_id": "bbbbb04-dc45-58d3-a801-d6b4b00fbbbbb",
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
            "base_indicator_id": ProcessInput(
                title="base_indicator_id",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
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



        result = {
            "jobSummary": [],
            "results": []
        }
        current_indicator = ""
        result_list = []
        job_summary = KommonitorJobSummary()
        result = KommonitorResult()

        try:
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)

            # Extract all relevant inputs
            target_indicator_id = inputs["target_indicator_id"]
            base_indicator_id = inputs["base_indicator_id"]
            ref_indicator_id = inputs["reference_indicator_id"]
            target_spatial_units = inputs["target_spatial_units"]
            exclude_dates = inputs["target_time"]["excludeDates"] if "excludeDates" in inputs["target_time"] else []
            include_dates = inputs["target_time"]["includeDates"] if "includeDates" in inputs["target_time"] else []

            for target_unit_id in target_spatial_units:
                result.init_spatial_unit_result(target_unit_id)
                job_summary.init_spatial_unit_summary(target_unit_id)

                # Fetch indicator timeseries data
                base_data = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(base_indicator_id, target_unit_id)
                ref_data = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(ref_indicator_id, target_unit_id)
                target_data = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(target_indicator_id, target_unit_id)

                # Create a DataFrame for each indicator timeseries data and merge it
                base_indicator_df = dataio.indicator_timeseries_to_dataframe(base_data, base_indicator_id, target_unit_id)
                ref_indicator_df = dataio.indicator_timeseries_to_dataframe(ref_data, ref_indicator_id, target_unit_id)
                target_indicator_df = dataio.indicator_timeseries_to_dataframe(target_data, target_indicator_id, target_unit_id)

                # Get a DataFrame that contains dates for all input indicators
                df_list = [base_indicator_df, ref_indicator_df, target_indicator_df]
                dates_df = dataio.get_applicable_dates(df_list)

                # Candidate target dates are all dates, which potentially should be calculated depending on the execution mode
                candidate_target_dates = dataio.get_missing_target_dates(dates_df,
                                                                         target_id=target_indicator_id,
                                                                         input_ids=[base_indicator_id, ref_indicator_id],
                                                                         drop_input_na=False,
                                                                         mode=inputs["target_time"]["mode"],
                                                                         exclude_dates=exclude_dates,
                                                                         include_dates=include_dates)

                # Computable target dates ar all dates, which potentially should be calculated depending on the execution mode and for which all inputs have an existing value
                computable_target_dates = dataio.get_missing_target_dates(dates_df,
                                                                          target_id=target_indicator_id,
                                                                          input_ids=[base_indicator_id, ref_indicator_id],
                                                                          drop_input_na=True,
                                                                          mode=inputs["target_time"]["mode"],
                                                                          exclude_dates=exclude_dates,
                                                                          include_dates=include_dates)

                # determine missing timestamps for input datasets to add errors to jobSummary
                missing_input_timestamps = dataio.get_missing_input_timestamps(candidate_target_dates, dates_df, [base_indicator_id, ref_indicator_id])
                if missing_input_timestamps:
                    job_summary.add_missing_timestamp_error(resource_type="indicator", dataset_id="", timestamps=missing_input_timestamps)

                merged_df = base_indicator_df.merge(ref_indicator_df, how="left", on=["ID", "date"],
                                               suffixes=("_base", "_ref"))

                # Cast indicator value columns to be numeric
                merged_df["value_target"] = pd.to_numeric(merged_df["value_target"])
                merged_df["value_ref"] = pd.to_numeric(merged_df["value_ref"])

                # Use computable target dates to filter DataFrame for relevant rows
                merged_df = merged_df[merged_df["date"].isin(computable_target_dates)]

                # Drop rows where at least one input has an NA value
                merged_df = merged_df.dropna(subset=["value_target", "value_ref"])
                # TODO create error for missing features

                # Calculate percentage share
                merged_df["result"] = merged_df["value_target"] / merged_df["value_ref"] * 100

                # Convert DataFrame back again to required JSON format
                indicator_values = dataio.dataframe_to_indicator_timeseries(merged_df)

                result.add_indicator_values(indicator_values)

            outputs = {
                "jobSummary": job_summary.report,
                "results": result.report
            }

            return JobStatus.successful, outputs
        except ApiException as e:
            logger.error(f"Exception when calling DataManagementAPI: {e}")
            job_summary.add_data_management_api_error()
            result["jobSummary"].append(job_summary.get_api_client_error(e))
            return JobStatus.failed, result
