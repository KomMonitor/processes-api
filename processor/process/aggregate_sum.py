import os
from typing import Union

import prefect
from prefect import flow, get_run_logger
from prefect.filesystems import LocalFileSystem
from prefect.states import Failed, Completed

from pygeoapi.process.base import *

from .util import data_management_client, as_geojson
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect import schemas

import openapi_client
import geopandas as gpd


@flow(persist_result=True)
def aggregate_sum_flow(
        job_id: str,
        result_storage_block: str | None,
        process_description: schemas.ProcessDescription,
        execution_request: schemas.ExecuteRequest
) -> Union[schemas.JobStatusInfoInternal, prefect.states.State]:
    """This is a simple prefect flow.

  It complies with pygeoapi-prefect's requirements, namely:

  - The @flow decorator includes `persist_results=True`
  - Accepts the required input parameters (job_id, result_storage_block,
    process_description, execution_request)
  - Stores outputs using prefect block
  - Returns a status_info
  """
    # TODO: define nicer path
    os.mkdir("results/" + job_id)
    log_path = f"results/{job_id}/log.txt"
    filelogger = logging.FileHandler(log_path)
    filelogger.setLevel(logging.DEBUG)
    logger = get_run_logger()
    logger.logger.addHandler(filelogger)
    logger.debug("Starting execution...")

    # 1. retrieve inputs
    # 1.1. some may be mandatory
    try:
        spatial_unit_id = execution_request.inputs["spatial_unit_id"].root
        georesource_id = execution_request.inputs["georesource_id"].root
        target_date = execution_request.inputs["target_date"].root
    except KeyError as e:
        logger.error(e)
        raise JobError(f"Missing a required property: {e}")

    generated_outputs = {
        "log": schemas.OutputExecutionResultInternal(
            location=log_path,
            media_type="plain/text",
        )
    }

    # result_path: str = "None"
    try:
        api_client = data_management_client(logger, execution_request, private=False)
        georesources_controller = openapi_client.GeorecourcesPublicControllerApi(api_client)
        spatial_units_controller = openapi_client.SpatialUnitsPublicControllerApi(api_client)
        target_col = f"WERT_{target_date}"

        # Fallback to WGS:84 as default CRS
        base_unit = as_geojson(spatial_units_controller.get_all_spatial_unit_features_by_id1(spatial_unit_id))
        crsDef = base_unit.get("crs", {"type": "name", "properties": {"name": "EPSG:4326"}})
        indicator = gpd.GeoDataFrame().from_features(base_unit, crs=crsDef.get("properties").get("name"))

        # init indicator default value
        indicator = indicator.assign(**{target_col: [0] * indicator.index.size})

        # get georesource features
        georesource_features = as_geojson(
            georesources_controller.get_all_public_georesource_features_by_id(georesource_id))
        georesources = gpd.GeoDataFrame().from_features(georesource_features, crs=crsDef.get("properties").get("name"))

        # join and aggregate
        joined = gpd.sjoin(georesources[['ID', 'geometry']], indicator[['ID', 'geometry']], how="inner", predicate="within")
        aggregated = joined.groupby('ID_right').count().reset_index()[['ID_right', 'ID_left']]
        indicator.update(aggregated.rename(columns={"ID_right": "ID", "ID_left": target_col}))

        # dump into file
        storage = LocalFileSystem()
        indicator_path = f"results/{job_id}/indicator.geo.json"
        storage.write_path(indicator_path, indicator.to_json().encode('utf-8'))

        generated_outputs["indicator"] = schemas.OutputExecutionResultInternal(
            location=indicator_path,
            media_type="application/geo+json",
        )
        return Completed(data=schemas.JobStatusInfoInternal(
            jobID=job_id,
            processID=process_description.id,
            status=schemas.JobStatus.successful,
            generated_outputs=generated_outputs
        ))

    except Exception as e:
        logger.error(f"Failed execution: {e}")
        return Failed(message="How did this happen!?", data=schemas.JobStatusInfoInternal(
            jobID=job_id,
            processID=process_description.id,
            status=schemas.JobStatus.failed,
            generated_outputs=generated_outputs
        ))


class AggregateSumFlowProcessor(BasePrefectProcessor):
    process_flow = aggregate_sum_flow
    result_storage_block = None
    process_description = schemas.ProcessDescription(
        id="aggregate_sum",
        version="0.0.1",
        title="Share of unemployed people in given spatial Unit",
        example={},
        jobControlOptions=[
            schemas.ProcessJobControlOption.SYNC_EXECUTE
        ],
        inputs={
            "spatial_unit_id": schemas.ProcessInput(
                title="spatial_unit_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "georesource_id": schemas.ProcessInput(
                title="georesource_id",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            ),
            "target_date": schemas.ProcessInput(
                title="target_date",
                schema=schemas.ProcessIOSchema(type=schemas.ProcessIOType.STRING)
            )
        },
        outputs={
            "log": schemas.ProcessOutput(
                schema=schemas.ProcessIOSchema(
                    type=schemas.ProcessIOType.STRING,
                    contentMediaType="text/plain",
                )
            ),
            "indicator": schemas.ProcessOutput(
                schema=schemas.ProcessIOSchema(
                    type=schemas.ProcessIOType.OBJECT,
                    contentMediaType="application/geo+json",
                )
            )
        },
    )
