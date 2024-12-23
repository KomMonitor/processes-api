from typing import Dict, Optional

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from processor.process.base import KommonitorProcess, KommonitorProcessConfig
from processor.process.util.geojson import as_geojson


class ShareUnemployed(KommonitorProcess):
    process_description = ProcessDescription(
        id="share-unemployed",
        version="0.0.1",
        title="Share of unemployed people in given spatial Unit",
        example={
            "population_georesource_id": "cccca04-cc57-48d3-a801-d6b4b00fcccc",
            "unemployed_georesource_id": "aaaaa04-cc57-48d3-a801-d6b4b00faaaa",
            "target_spatial_unit": "bbbba04-cc57-48d3-a801-d6b4b00fbbbb",
            "target_date": "2000-01-01"
        },
        additional_parameters=AdditionalProcessIOParameters(
            parameters=[
                Parameter(
                    name="legend",
                    value=["Share of unemployed people in given spatial Unit"]
                ),
                Parameter(
                    name="formula",
                    value=["(unemployed_count / population_count) / 100"]
                ),
            ]
        ),
        jobControlOptions=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs={
            "population_georesource_id": ProcessInput(
                title="population_georesource_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "unemployed_georesource_id": ProcessInput(
                title="unemployed_georesource_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "target_spatial_unit": ProcessInput(
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
            georesources_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            indicator = {}

            response = georesources_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                inputs["population_georesource_id"], inputs["target_spatial_unit"])
            # Iterate population
            for feat in response:
                feature_id = feat["fid"]

                population = feat[f"DATE_{inputs['target_date']}"]
                if population is None:
                    population = 0
                    logger.error(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                                 f"time series value for targetDate '{inputs['target_date']}")

                indicator[feature_id] = {
                    "feature_id": feature_id,
                    "value": None,
                    "population": float(population)
                }

            # Iterate unemployed
            response = georesources_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                inputs["unemployed_georesource_id"], inputs["target_spatial_unit"])
            for feat in response:
                feature_id = feat["fid"]

                unemployed = feat[f"DATE_{inputs['target_date']}"]
                if unemployed is None:
                    logger.error(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                                 f"time series value for targetDate '{inputs['target_date']}")
                else:
                    # Calculate percentage
                    indicator[feature_id]["value"] = (float(unemployed) / indicator[feature_id]["population"]) / 100

            return JobStatus.successful, {"result": indicator}
        except ApiException as e:
            logger.error(f"Exception when calling DataManagementAPI: {e}")
            return JobStatus.failed, None
