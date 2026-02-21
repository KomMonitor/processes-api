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
    from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType, IndicatorExport, GeoressourceExport, TargetTime
except ImportError:
    from processor.process.pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType, IndicatorExport, GeoressourceExport, TargetTime

try:
    from ..base import KommonitorProcessConfig, KommonitorResult, DataManagementException, store_output_as_file, \
        KOMMONITOR_DATA_MANAGEMENT_URL, setup_logging, data_management_client, format_inputs, generate_flow_run_name
except ImportError:
    from processor.process.base import KommonitorProcessConfig, KommonitorResult, DataManagementException, store_output_as_file, \
        KOMMONITOR_DATA_MANAGEMENT_URL, setup_logging, data_management_client, format_inputs, generate_flow_run_name

try:
    from ..util import dataio
except ImportError:
    from processor.process.util import dataio


# this name should be set for @flow(name='<processName>') and within detailed_process_description as 
# additional_parameters.parameters[0].value[0].apiName
# this is necessary in order to have a comparable name between prefect schedules and pygeoAPI process descriptions
processName = "export_test"
@flow(persist_result=True, name=processName, flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return ExportTest.execute_process_flow(ExportTest.run, job_id, execution_request)

class ExportTest(BasePrefectProcessor):
    process_flow = process_flow
    detailed_process_description = ProcessDescription(
        id=processName,
        version="0.0.1",
        title="ExportTest",
        description= "Test",
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

            "spatial_unit": ProcessInput(
                id="spatial_unit",
                title="Raumebenen-Export Konfiguration",
                description="Exportiert mehrere Indikatoren für eine spezifische Raumebene.",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    properties={
                        "spatial_unit_id": ProcessIOSchema(type_=ProcessIOType.STRING),
                        "indicators": ProcessIOSchema(
                            type_=ProcessIOType.ARRAY,
                            items=ProcessIOSchema(
                                type_=ProcessIOType.OBJECT,
                                properties={
                                    "indicator_id": ProcessIOSchema(type_=ProcessIOType.STRING),
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
                        ),
                        "download_format": ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING))
                    }
                )
            ),

        },
        outputs = {}
    )
    def __init__(self, processor_def: dict):
        super().__init__(processor_def)

    @property
    def process_description(self) -> schemas.ProcessDescription:
        description = self.detailed_process_description
        return description

    @staticmethod
    def execute_process_flow(
            run: Task,
            job_id: str,
            execution_request: schemas.ExecuteRequest
    ) -> dict:
        ## Setup
        flow_id = runtime.flow_run.name
        logger = setup_logging(flow_id)
        logger.info(f"Flow run name: {flow_id}")

        inputs = format_inputs(execution_request)
        config = KommonitorProcessConfig(flow_id, inputs, f"{flow_id}/output-result.txt")
        dmc = data_management_client(logger, execution_request, True)

        ## Run process
        result = run(config=config, logger=logger, data_management_client=dmc)
        print(result)

        return store_output_as_file(flow_id, result, logger)

    # run Method has to be implemented for all KomMonitor Skripts
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
