import ast
import io
import json

from openapi_client import GeoresourcePOSTInputType
from prefect import flow, get_run_logger
from prefect.filesystems import LocalFileSystem

from pygeoapi.process.base import *

from .util import data_management_client, as_geojson
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect import schemas

import openapi_client
from openapi_client.rest import ApiException

import geopandas as gpd


@flow(persist_result=True)
def simple_flow(
        job_id: str,
        result_storage_block: str | None,
        process_description: schemas.ProcessDescription,
        execution_request: schemas.ExecuteRequest
) -> schemas.JobStatusInfoInternal:
    """This is a simple prefect flow.

  It complies with pygeoapi-prefect's requirements, namely:

  - The @flow decorator includes `persist_results=True`
  - Accepts the required input parameters (job_id, result_storage_block,
    process_description, execution_request)
  - Stores outputs using prefect block
  - Returns a status_info
  """
    logger = get_run_logger()
    logger.debug("Starting execution...")

    # 1. retrieve inputs
    # 1.1. some may be mandatory
    try:
        population_georesource_id = execution_request.inputs["population_georesource_id"].root
        unemployed_georesource_id = execution_request.inputs["unemployed_georesource_id"].root
        target_spatial_unit_id = execution_request.inputs["target_spatial_unit_id"].root
        target_date = execution_request.inputs["target_date"].root
    except KeyError as e:
        raise JobError(f"Missing a required property: {e}")

    result_path: str = "None"
    try:
        api_client = data_management_client()
        georesources_controller = openapi_client.GeorecourcesControllerApi(api_client)
        spatial_units_controller = openapi_client.SpatialUnitsControllerApi(api_client)

        indicator = {}

        # Iterate population
        for feat in as_geojson(georesources_controller.get_all_georesource_features_by_id(population_georesource_id)):
            feature_id = feat["properties"]["ID"]

            population = feat[f"DATE_{target_date}"]
            if population is None:
                population = 0
                print(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                      f"time series value for targetDate '{target_date}")

            indicator[feature_id] = {
                "feature_id": feature_id,
                "value": None,
                "population": population
            }

        # Iterate unemployed
        for feat in as_geojson(georesources_controller.get_all_georesource_features_by_id(unemployed_georesource_id)):
            feature_id = feat["properties"]["ID"]

            unemployed = feat[f"DATE_{target_date}"]
            if unemployed is None:
                population = 0
                print(f"WARNING: the feature with featureID '{feature_id}' does not contain a "
                      f"time series value for targetDate '{target_date}")

            indicator[feature_id]["value"] = (unemployed / indicator[feature_id]["population"]) / 100




    except ApiException as e:
        print("Exception when calling GeorecourcesControllerApi->add_georesource_as_body: %s\n" % e)

    # 5. Return a status info object
    return schemas.JobStatusInfoInternal(
        jobID=job_id,
        processID=process_description.id,
        status=schemas.JobStatus.successful,
        #        generated_outputs={
        #            "result": schemas.OutputExecutionResultInternal(
        #                location=result_path,
        #                media_type=(
        #                    process_description.outputs["result"].schema_.content_media_type
        #                ),
        #            )
        #        },
    )


class SimpleFlowProcessor(BasePrefectProcessor):
    process_flow = simple_flow
    result_storage_block = None
    process_description = schemas.ProcessDescription(
        id="share-unemployed",
        version="0.0.1",
        title="Share of unemployed people in given spatial Unit",
        example={},
        jobControlOptions=[
            schemas.ProcessJobControlOption.SYNC_EXECUTE
        ],
        inputs={
            "population_georesource_id": schemas.ProcessInput(
                title="population_georesource_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "unemployed_georesource_id": schemas.ProcessInput(
                title="unemployed_georesource_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "target_spatial_unit": schemas.ProcessInput(
                title="target_spatial_unit_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "target_date": schemas.ProcessInput(
                title="target_date",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            )
        },
        outputs={},
    )
