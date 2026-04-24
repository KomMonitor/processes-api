import logging
import openapi_client
import json
import os
import shutil
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
    
processName = "multiple_export"
@flow(persist_result=True, name=processName, flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return MultipleExport.execute_process_flow(MultipleExport.run, job_id, execution_request)

class MultipleExport(ExportProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id=processName,
        version="0.0.1",
        title="MultipleExport",
        description= "Export mehrerer Indikatoren, jeweils kombiniert für mehrere Raumebene. Es wird nur der GeoPackage Download unterstützt. Für jeden Indikator erfolgt ein Export für mehrere gewählte Raumebene in einem GeoPackage, wobei es für jede Raumebene einen eigenen Layer im GeoPackage gibt.",
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
            "multiple_export": ProcessInput(
                id="multiple_export",
                title="Multi-Export Konfiguration",
                description="Sammel-Export für verschiedene Indikatoren.",
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
                                    )
                                }
                            )
                        )
                    }
                )
            )
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

        try:
            # Load inputs
            inputs = config.inputs
            print(inputs)
            # Extract all relevant inputs
            # in this case every IndicatorExport item of indicators has only one spatial unit id
            crs, indicators = pykmhelper.process_multiple_export_inputs(inputs)

            # 3. Generate result || Main Script
            if data_management_client.configuration.access_token:
                indicators_controller = openapi_client.IndicatorsApi(data_management_client)
            else:
                indicators_controller = openapi_client.IndicatorsPublicApi(data_management_client)

            PROCESS_RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', "/tmp")
            path = rf"{PROCESS_RESULTS_DIR}\{flow_id}\export_data"

            if not os.path.isdir(path):
                os.mkdir(path)
            try:
                if len(indicators) > 0:
                    for indicator in indicators:
                        indicator.add_geodataframes(indicators_controller)
                        indicator.filter_target_times()
                        indicator.export_gpkg_multiple_export(path, crs)
            except RuntimeError as e:
                logger.error(f"A processing-error occurred during multiple indicator export: {e}")
                raise RuntimeError(f"A processing-error occurred during multiple indicator export: {e}")

            shutil.make_archive(path, "zip", path)
            shutil.rmtree(path)

            return {
                "status": "successful",
                "file": {
                    "href": f"{config.server_url}/exports/{job_id}/export_data.zip",
                    "rel": "enclosure",
                    "type": "application/octet-stream",
                    "title": f"{flow_id}/export_data.zip"
            }}
        except Exception as e:
          logger.error(f"An Error occurred during multiple export: {e}")
          return {
               "status": "failed",
               "error": str(e)
           }
        