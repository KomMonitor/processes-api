import ast
import io
import json

from openapi_client import GeoresourcePOSTInputType
from prefect import flow, get_run_logger
from prefect.filesystems import LocalFileSystem

from pygeoapi.process.base import *

from .util import data_management_client
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
        georesource_id = execution_request.inputs["georesource_id"].root
        crs = execution_request.inputs["crs"].root
    except KeyError as e:
        raise JobError(f"Missing a required property: {e}")

    result_path: str = "None"
    try:
        api_client = data_management_client()
        georesources_controller = openapi_client.GeorecourcesControllerApi(api_client)

        # Add a new geo-resource
        georesource = georesources_controller.get_georesource_by_id(georesource_id)
        features = georesources_controller.get_all_georesource_features_by_id(georesource_id)
        # print("The response of GeorecourcesControllerApi->get_georesources:\n")
        print(features)

        # Uses literal_eval as feature is encoded with single quotes
        geojson = ast.literal_eval(features)
        # Fallback to WGS:84 as default CRS
        crsDef = geojson.get("crs", {"type": "name", "properties": {"name": "EPSG:4326"}})
        gdf = gpd.GeoDataFrame().from_features(geojson, crs=crsDef.get("properties").get("name"))
        # if gdf.crs is None:
        #    gdf.set_crs("EPSG:4326", inplace=True)

        # Transform to requested
        gdf = gdf.to_crs(crs)

        outputs = gdf.to_json()

        storage = LocalFileSystem()
        result_path = f"{job_id}/output-result.txt"

        storage.write_path(result_path, outputs.encode('utf-8'))

        template = georesource.to_dict()
        template["geoJsonString"] = gdf.to_json()
        template["periodOfValidity"] = template.get("availablePeriodsOfValidity")[0]
        template["datasetName"] = "krank_reprojected_reprojected"

        payload: GeoresourcePOSTInputType = GeoresourcePOSTInputType.from_dict(template)
        georesources_controller.add_georesource_as_body(payload)

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
        id="reproject",
        version="0.0.2",
        title="Reproject Georesource",
        example={
            "inputs": {
                "input_georesource_id": "aa43848b-d30e-4d4a-b152-000000000000",
                "crs": "EPSG:4326",
                "output_georesource_name": ""
            }
        },
        jobControlOptions=[
            schemas.ProcessJobControlOption.SYNC_EXECUTE
        ],
        inputs={
            "input_georesource_id": schemas.ProcessInput(
                title="input_georesource_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "crs": schemas.ProcessInput(
                title="crs",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "output_georesource_name": schemas.ProcessInput(
                title="output_georesource_name",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
        },
        outputs={},
    )
