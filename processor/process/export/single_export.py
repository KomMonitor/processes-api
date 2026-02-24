import logging
import openapi_client
import json
import os
import geopandas as gpd
from openapi_client import ApiClient, ApiException
from prefect import task, get_run_logger, Task, runtime, flow
from prefect.cache_policies import NO_CACHE
from pygeoapi_prefect import schemas
from pygeoapi_prefect.process.base import BasePrefectProcessor
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType, ProcessDescription, ProcessJobControlOption, AdditionalProcessIOParameters, Parameter

try:
    from .. import pykmhelper
except ImportError:
    from processor.process import pykmhelper
    
try:
    from ..base import DataManagementException, store_output_as_file, KommonitorProcessConfig, \
        KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name
except ImportError:
    from processor.process.base import DataManagementException, store_output_as_file, KommonitorProcessConfig, \
        KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name

try:
    from ..base_export import ExportProcess
except:
    from ..base_export import ExportProcess
    
processName = "single_export"
@flow(persist_result=True, name=processName, flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return SingleExport.execute_process_flow(SingleExport.run, job_id, execution_request)

class SingleExport(ExportProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id=processName,
        version="0.0.1",
        title="SingleExport",
        description= "Export mehrerer Indikatoren und Georessourcen als Einzeldatensätze in einem bestimmten Format. Die Ausgabe der Einzeldatensätze erfolgt zusammen in einem ZIP-Ordner.",
        example={},
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        additional_parameters=AdditionalProcessIOParameters(
            parameters=[
                Parameter(
                    name="kommonitorUiParams",
                    value=[{}]
                )
            ]
        ),

        inputs = {
            "single_export": ProcessInput(
                id="single_export",
                title="Einzel-Export Konfiguration",
                description="Konfiguration für den Export spezifischer Indikatoren und Georessourcen.",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    properties={
                        "indicators": ProcessIOSchema(
                            type_=ProcessIOType.ARRAY,
                            items=ProcessIOSchema(
                                type_=ProcessIOType.OBJECT,
                                properties={
                                    "indicator_id": ProcessIOSchema(type_=ProcessIOType.STRING),
                                    "spatial_unit_ids": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)),
                                    "target_time": ProcessIOSchema(
                                        type_=ProcessIOType.OBJECT,
                                        properties={
                                            "mode": ProcessIOSchema(type_=ProcessIOType.STRING, enum=["SINGLE", "START_END", "ALL"]),
                                            "include_dates": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)),
                                            "start_date": ProcessIOSchema(type_=ProcessIOType.STRING),
                                            "end_date": ProcessIOSchema(type_=ProcessIOType.STRING)
                                        },
                                        required=["mode"]
                                    ),
                                    "download_format": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)) # Mehrfachauswahl möglich
                                }
                            )
                        ),
                        "georessources": ProcessIOSchema(
                            type_=ProcessIOType.ARRAY,
                            items=ProcessIOSchema(
                                type_=ProcessIOType.OBJECT,
                                properties={
                                    "georessource_id": ProcessIOSchema(type_=ProcessIOType.STRING),
                                    "target_time": ProcessIOSchema(
                                        type_=ProcessIOType.OBJECT,
                                        properties={
                                            "mode": ProcessIOSchema(type_=ProcessIOType.STRING, enum=["SINGLE", "START_END", "ALL"]),
                                            "include_dates": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING)),
                                            "start_date": ProcessIOSchema(type_=ProcessIOType.STRING),
                                            "end_date": ProcessIOSchema(type_=ProcessIOType.STRING)
                                        },
                                        required=["mode"]
                                    ),
                                    "download_format": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING))
                                }
                            )
                        )
                    }
                )
            ),
        },
        outputs = {}
    )
    
    @staticmethod
    @task(cache_policy=NO_CACHE)
    def run(config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> dict:
        
        logger.debug("Starting execution...")

        # Load inputs
        inputs = config.inputs
        print(inputs)
        # Extract all relevant inputs
        indicators, georessources = pykmhelper.process_export_inputs(inputs)
        print(indicators)
        # 3. Generate result || Main Script    
        indicators_controller = openapi_client.IndicatorsApi(data_management_client)
        spatial_unit_controller = openapi_client.SpatialUnitsApi(data_management_client)

        raw_series = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_preload_content(indicators[0].indicator_id, indicators[0].spatial_unit_ids[0])
        data = json.loads(raw_series.data)

        gdf = gpd.GeoDataFrame.from_features(data["features"])

        PROCESS_RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', "/tmp")

        gdf.to_file(f"{PROCESS_RESULTS_DIR}/ExportTest.GeoJSON", driver="GeoJSON")
        print(gdf.head())
        return {
            "status": "successful",
            "file": {
                "href": "127.0.0.1:8099/exports/ExportTest.GeoJSON",
                "rel": "enclosure",
                "type": "application/octet-stream",
                "title": "ExportTest.GeoJSON"
        }}