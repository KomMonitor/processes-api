import logging
import openapi_client
import os
import shutil
import openpyxl
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
    
processName = "spatial_unit_export"
@flow(persist_result=True, name=processName, flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return SpatialUnitExport.execute_process_flow(SpatialUnitExport.run, job_id, execution_request)

class SpatialUnitExport(ExportProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id=processName,
        version="0.0.1",
        title="SpatialUnitExport",
        description= "Export mehrerer Indikatoren für eine Raumebene. Es wird nur der GeoPackage und CSV/Excel Download unterstützt. Für jeden Indikator dieser Raumebene gibt es einen eigenen Layer im GeoPackage. Beim CSV/Excel Export gibt es für jeden Indikator eine eigene Spalte.",
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
            "spatial_unit": ProcessInput(
                id="spatial_unit",
                title="Raumebenen-Export Konfiguration",
                description="Exportiert mehrere Indikatoren für eine spezifische Raumebene.",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    properties={
                        "spatial_unit_id": ProcessIOSchema(type_=ProcessIOType.STRING),
                        "crs": ProcessIOSchema(type_=ProcessIOType.STRING),
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
            crs, format, indicators = pykmhelper.process_spatial_unit_export_inputs(inputs)

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
                        if "GEOPACKAGE" in format:
                            indicator.export_gpkg_spatial_unit_export(path, crs)

                    if "CSV" in format:
                        filename, merged_gdf = pykmhelper.merge_multiple_dataframes(indicators)
                        merged_gdf.to_csv(rf"{path}\{filename}.csv")

                    if "EXCEL" in format:
                        filename, merged_gdf = pykmhelper.merge_multiple_dataframes(indicators)
                        merged_gdf.to_excel(rf"{path}\{filename}.xlsx")
            except RuntimeError as e:
                logger.error(f"A processing-error occurred during spatial unit indicator export: {e}")

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
          logger.error(f"An Error occurred during spatial unit export: {e}")
          return None