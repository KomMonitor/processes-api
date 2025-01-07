from typing import Dict, Optional

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from processor.process.base import KommonitorProcess, KommonitorProcessConfig
from processor.process.util.geojson import as_geojson


class PercentageShare(KommonitorProcess):
    process_description = ProcessDescription(
        id="percentage-share",
        version="0.0.1",
        title="Percentage share of an indicator to a reference indicator in a given spatial unit",
        example={
            "indicator_id": "cccca04-cc57-48d3-a801-d6b4b00fcccc",
            "reference_indicator_id": "aaaaa04-cc57-48d3-a801-d6b4b00faaaa",
            "target_spatial_unit_id": "bbbba04-cc57-48d3-a801-d6b4b00fbbbb",
            "target_date": "2000-01-01"
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
        jobControlOptions=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs={
            "indicator_id": ProcessInput(
                title="indicator_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "reference_indicator_id": ProcessInput(
                title="reference_indicator_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "target_spatial_unit_id": ProcessInput(
                title="target_spatial_unit_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "target_date": ProcessInput(
                title="target_date",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            )
        },
        outputs={
            "result": ProcessOutput(
                schema=ProcessIOSchema(
                    type=ProcessIOType.OBJECT,
                    contentMediaType="application/json",
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
        logger.debug("Starting execution...")

        try:
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            indicator = {}

            response = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                inputs["reference_indicator_id"], inputs["target_spatial_unit_id"])
            # Iterate population
            for feat in response:
                feature_id = feat["fid"]

                ref_value = feat[f"DATE_{inputs['target_date']}"]
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
                inputs["indicator_id"], inputs["target_spatial_unit_id"])
            for feat in response:
                feature_id = feat["fid"]

                value = feat[f"DATE_{inputs['target_date']}"]
                if value is None:
                    logger.error(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                                 f"time series value for targetDate '{inputs['target_date']}")
                else:
                    # Calculate percentage
                    indicator[feature_id]["value"] = (float(value) / indicator[feature_id]["ref_value"]) * 100

            return JobStatus.successful, {"result": indicator}
        except ApiException as e:
            logger.error(f"Exception when calling DataManagementAPI: {e}")
            return JobStatus.failed, None
