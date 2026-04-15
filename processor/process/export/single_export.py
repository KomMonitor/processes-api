import logging
import openapi_client
import json
import shutil
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
                        "crs": ProcessIOSchema(type_=ProcessIOType.STRING),
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
            data_management_client: ApiClient,
            job_id: str,
            flow_id: str) -> dict:
        
        logger.debug("Starting execution...")

        # Load inputs
        inputs = config.inputs
        try:
            # Extract all relevant inputs
            crs, indicators, georesources = pykmhelper.process_single_export_inputs(inputs)

            # 3. Generate result || Main Script
            indicators_controller = openapi_client.IndicatorsApi(data_management_client)
            georesources_controller = openapi_client.GeoresourcesApi(data_management_client)

            PROCESS_RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', "/tmp")
            path = rf"{PROCESS_RESULTS_DIR}\{flow_id}\export_data"
            
            if not os.path.isdir(path):
                os.mkdir(path)

            try:
                if len(indicators) > 0:
                    for indicator in indicators:
                        indicator.add_geodataframes(indicators_controller)
                        indicator.filter_target_times()
                        indicator.export_files_single_export(path, crs)
            except RuntimeError as e:
                logger.error(f"A processing-error occurred during indicators single export: {e}")

            try:
                if len(georesources) > 0:
                    for georesource in georesources:
                        georesource.add_geodataframe(georesources_controller)
                        georesource.filter_target_times()
                        georesource.export_files_single_export(path, crs)
            except RuntimeError as e:
                logger.error(f"A processing-error occurred during georesources single export: {e}")

            shutil.make_archive(path, "zip", path)
            shutil.rmtree(path)

            return {
                "status": "successful",
                "file": {
                    "href": f"127.0.0.1:8099/exports/{job_id}/export_data.zip",
                    "rel": "enclosure",
                    "type": "application/octet-stream",
                    "title": f"{flow_id}/export_data.zip"
            }}
        except Exception as e:
           logger.error(f"An Error occurred during single export: {e}")
           return None