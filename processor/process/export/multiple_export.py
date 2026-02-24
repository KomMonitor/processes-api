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

        return None
        