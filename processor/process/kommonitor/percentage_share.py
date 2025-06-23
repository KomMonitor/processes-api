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

# from pandas import isnull
import pandas as pd

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
    from ..util import dataio
except ImportError:
    from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name
    from processor.process.util import dataio


@flow(persist_result=True, name="hello_world", flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(PercentageShare.run, job_id, execution_request)


class PercentageShare(KommonitorProcess):

    process_flow = process_flow

    detailed_process_description = ProcessDescription(
        id="percentage-share",
        version="0.0.1",
        title="Prozentualer Anteil mehrerer Basisindikatoren von einem Referenzindikator",
        description= "Mindestens ein (Basis-)Indikator muss angegeben werden. Bei mehreren wird die Gesamtsumme der (Basis-)Indikatoren durch den Wert des Referenzindikators dividiert",
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
                    name="kommonitorUiParams",
                    value=[{
                        "titleShort": "Prozentualer Anteil (Quotient zwischen Basis-Indikatoren und einem Referenzindikator)",
                        "apiName": "indicator_share_percentage",
                        "formula": "$$ \frac{\sum_{n=1}^{m} I_{n}}{I_{ref}} \times 100 $$",
                        "legend": "<br/>$I_{n}$ = Basis-Indikatoren <br/>$I_{ref}$ = Referenzindikator ",
                        "dynamicLegend": "${list_baseIndicators} <br/>$ I_{ref} $: ${refIndicatorSelection.indicatorName} [ ${refIndicatorSelection.unit} ]<br/>",
                        "inputBoxes": [
                           {
                            "id": "reference_id",
                            "title": "Notwendiger Referenzindikator (Divisor)",
                            "description": "",
                            "contents": [
                                "reference_id"
                            ]
                            },
                            {
                            "id": "computation_ids",
                            "title": "Notwendige (Basis-)Indikatoren (Dividend)",
                            "description": "",
                            "contents": [
                                "computation_ids"
                            ]
                            }
                        ]
                    }]
                )
            ]
        ),
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs=KommonitorProcess.common_inputs | {
            "computation_ids": ProcessInput(
                title="Notwendige (Basis-)Indikatoren (Dividend)",
                description="Auswahl der für die Berechnung erforderlichen (Basis-)Indikatoren",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.ARRAY,
                    items=ProcessIOSchema(type_=ProcessIOType.STRING),
                    min_items=1
                )
            ),
            "reference_id": ProcessInput(
                title="Notwendiger Referenzindikator (Divisor)",
                description="Auswahl des für die Berechnung erforderlichen Referenzindikators",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            )
        },
        outputs = KommonitorProcess.common_output
    )


    @staticmethod
    @task(cache_policy=NO_CACHE)
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> Tuple[JobStatus, KommonitorResult, KommonitorJobSummary]:

        logger.debug("Starting execution...")

        # Load inputs
        inputs = config.inputs
        # Extract all relevant inputs
        target_indicator_id = inputs["target_indicator_id"]
        base_indicator_id = inputs["base_indicator_id"]
        ref_indicator_id = inputs["reference_indicator_id"]
        target_spatial_units = inputs["target_spatial_units"]
        exclude_dates = inputs["target_time"]["excludeDates"] if "excludeDates" in inputs["target_time"] else []
        include_dates = inputs["target_time"]["includeDates"] if "includeDates" in inputs["target_time"] else []

        # Init object to store computation results
        result = KommonitorResult()
        job_summary = KommonitorJobSummary()

        try:
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            spatial_unit_controller = openapi_client.SpatialUnitsControllerApi(data_management_client)

            for target_unit_id in target_spatial_units:
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(target_unit_id)
                job_summary.init_spatial_unit_summary(target_unit_id)

                # Fetch spatial unit metadata since result data needs spatial unit name instead of its ID
                su_metadata = fetch_spatial_unit_metadata(spatial_unit_controller, target_unit_id, job_summary, logger)
                if su_metadata is None:
                    job_summary.complete_spatial_unit_summary()
                    continue

                # Fetch indicator timeseries data
                base_data = fetch_indicator_timeseries(indicators_controller, base_indicator_id, target_unit_id, job_summary, logger)
                print(base_data)
                ref_data = fetch_indicator_timeseries(indicators_controller, ref_indicator_id, target_unit_id, job_summary, logger)
                target_data = fetch_indicator_timeseries(indicators_controller, target_indicator_id, target_unit_id, job_summary, logger)

                if base_data is None or ref_data is  None or target_data is  None:
                    job_summary.complete_spatial_unit_summary()
                    continue
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
                for missing in missing_input_timestamps:
                    job_summary.add_missing_timestamp_error(resource_type="indicator", dataset_id=missing["id"], timestamps=[d.strftime("%Y-%m-%d") for d in missing["missingTimestamps"]])

                merged_df = base_indicator_df.merge(ref_indicator_df, how="left", on=["ID", "date"],
                                               suffixes=("_base", "_ref"))

                # Cast indicator value columns to be numeric
                merged_df["value_base"] = pd.to_numeric(merged_df["value_base"])
                merged_df["value_ref"] = pd.to_numeric(merged_df["value_ref"])

                # Use computable target dates to filter DataFrame for relevant rows
                merged_df = merged_df[merged_df["date"].isin(computable_target_dates)]

                # Drop rows where at least one input has an NA value
                merged_df = merged_df.dropna(subset=["value_base", "value_ref"])
                # TODO create error for missing features

                # Calculate percentage share
                merged_df["result"] = merged_df["value_base"] / merged_df["value_ref"] * 100

                # Convert DataFrame back again to required JSON format
                indicator_values = dataio.dataframe_to_indicator_timeseries(merged_df)

                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates([d.strftime("%Y-%m-%d") for d in computable_target_dates])
                job_summary.add_modified_resource(KOMMONITOR_DATA_MANAGEMENT_URL, target_indicator_id, target_unit_id)
                job_summary.complete_spatial_unit_summary()

                result.add_indicator_values(indicator_values)
                result.complete_spatial_unit_result()
            return JobStatus.successful, result, job_summary
        except ApiException as e:
            logger.error(f"Exception when instantiating DataManagementAPI client: {e}")
            return JobStatus.failed, result, job_summary
