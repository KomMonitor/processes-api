from typing import Dict, Optional

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from ..base import KommonitorProcess, KommonitorProcessConfig


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


            response = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                reference_indicator_id, target_unit_id)
            # Iterate population
            for feat in response:
                feature_id = feat["fid"]

                ref_value = feat[f"DATE_{target_time}"]
                if ref_value is None:
                    # TODO: None must be None and not 0. Otherwise calculated indicator is misleading and
                    #  calculation may cause an error
                    ref_value = 0
                    logger.error(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                                 f"time series value for targetDate '{inputs['target_date']}")

                indicator[feature_id] = {
                    "feature_id": feature_id,
                    "value": None,
                    "ref_value": float(ref_value)
                }

            # Iterate unemployed
            response = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                target_indicator_id, target_unit_id)
            for feat in response:
                feature_id = feat["fid"]

                value = feat[f"DATE_{target_time}"]
                if value is None:
                    logger.error(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                                 f"time series value for targetDate '{inputs['target_date']}")
                else:
                    # Calculate percentage
                    indicator[feature_id]["value"] = (float(value) / indicator[feature_id]["ref_value"]) * 100

            result = {
                "jobSummary": [],
                "results": [
                    {
                        "applicableSpatialUnit": target_unit_id,
                        "indicatorValues": []
                    }
                ]
            }
            for feature in indicator.values():
                result["results"][0]["indicatorValues"].append(
                    {
                        "spatialReferenceKey": feature["feature_id"],
                        "valueMapping": [
                            {
                                "indicatorValue": feature["value"],
                                "timestamp": target_time
                            }
                        ]
                    }
                )

            return JobStatus.successful, result
        except ApiException as e:
            logger.error(f"Exception when calling DataManagementAPI: {e}")
            return JobStatus.failed, None
