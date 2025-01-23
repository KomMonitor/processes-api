import ast
from typing import Dict, Optional

from openapi_client import ApiClient, GeorecourcesControllerApi, GeoresourcePOSTInputType, ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from ..base import KommonitorProcess, KommonitorProcessConfig
from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, OutputExecutionResultInternal

import geopandas as gpd


class Reproject(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="reproject",
        version="0.0.2",
        title="Reproject Georesource and persists result to local file.",
        example={
            "inputs": {
                "input_georesource_id": "aa43848b-d30e-4d4a-b152-000000000000",
                "crs": "EPSG:4326",
                "output_georesource_name": "aaaaaaaa-d30e-4d4a-b152-000000001111"
            }
        },
        jobControlOptions=[
            ProcessJobControlOption.SYNC_EXECUTE
        ],
        inputs={
            "input_georesource_id": ProcessInput(
                title="input_georesource_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "crs": ProcessInput(
                title="crs",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "output_georesource_name": ProcessInput(
                title="output_georesource_name",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "target_indicator_id": ProcessInput(
                title="target_indicator_id",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            ),
            "target_spatial_units": ProcessInput(
                title="target_spatial_units",
                schema=ProcessIOSchema(type=ProcessIOType.ARRAY, items=[ProcessIOSchema(type=ProcessIOType.STRING)],
                                       min_items=1)
            ),
            "target_time ": ProcessInput(
                title="target_time",
                schema=ProcessIOSchema(
                    type=ProcessIOType.OBJECT,
                    properties=ProcessIOSchema(allOf=[ProcessIOSchema(title="mode", type=ProcessIOType.STRING),
                                                      ProcessIOSchema(title="includeDates", type=ProcessIOType.ARRAY,
                                                                      items=[
                                                                          ProcessIOSchema(type=ProcessIOType.STRING)]),
                                                      ProcessIOSchema(title="excludeDates", type=ProcessIOType.ARRAY,
                                                                      items=[
                                                                          ProcessIOSchema(type=ProcessIOType.STRING)])
                                                      ]
                                               )
                )
            ),
            "execution_interval ": ProcessInput(
                title="execution_interval",
                schema=ProcessIOSchema(type=ProcessIOType.STRING)
            )
        },
        outputs={}
    )

    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> (JobStatus, Optional[Dict[str, OutputExecutionResultInternal]]):

        # 1. Load inputs
        output_georesource_name = config.inputs["output_georesource_name"]
        georesource_id = config.inputs["georesource_id"]
        crs = config.inputs["crs"]

        # 2. Log some useful stuff
        logger.debug("Starting execution...")

        try:

            georesources_controller = GeorecourcesControllerApi(data_management_client)

            # Add a new geo-resource
            georesource = georesources_controller.get_georesource_by_id(georesource_id)
            features = georesources_controller.get_all_georesource_features_by_id(georesource_id)
            # print("The response of GeorecourcesControllerApi->get_georesources:\n")
            # print(features)

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

            template = georesource.to_dict()
            template["geoJsonString"] = gdf.to_json()
            template["periodOfValidity"] = template.get("availablePeriodsOfValidity")[0]
            template["datasetName"] = output_georesource_name

            # do not persist to database but only to local file for now
            payload: GeoresourcePOSTInputType = GeoresourcePOSTInputType.from_dict(template)
            georesources_controller.add_georesource_as_body(payload)

            # 4.1 Return success and result
            return JobStatus.successful, None
        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            logger.error(f"Exception when processing: {e}")
            return JobStatus.failed, None
