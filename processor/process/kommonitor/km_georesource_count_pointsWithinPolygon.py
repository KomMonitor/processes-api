import json
from typing import Tuple
import logging
import math

import openapi_client
from openapi_client import ApiClient
from prefect import task, flow
from prefect.cache_policies import NO_CACHE
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus
from pygeoapi_prefect import schemas
from pygeoapi_prefect.schemas import ProcessDescription, ProcessJobControlOption, Parameter, \
    AdditionalProcessIOParameters
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType

# from ..base import DataManagementException

try:
    from .. import pykmhelper
except ImportError:
    from processor.process import pykmhelper

try:
    from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
except ImportError:
    from processor.process.pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType

try:
    from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name
except ImportError:
    from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name


@flow(persist_result=True, name="km_georesource_count_pointsWithinPolygon", flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(KmGeoresourceCountPointsWithinPolygon.run, job_id, execution_request)

class KmGeoresourceCountPointsWithinPolygon(KommonitorProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id="km_georesource_count_pointsWithinPolygon",
        version="0.0.1",
        title="Anzahl Punkte in Polygon",
        description= "Auswahl einer punktbasierten Georessource, für die eine Punkt-in-Polygon Analyse durchgeführt wird, um die Anzahl der Punkte pro Raumeinheit zu erhalten. Optional können die Punktdaten anhand einer Objekteigenschaft sowie einem Filterwert dieser Objekteigenschaft gefiltert werden (z. B. Objekteigenschaft: Schulform, Filterwert: Grundschule, Operatoren: gleich/ungleich/enthält). Für numerische Werte lassen sich zudem Wertebereiche spezifizieren (z. B. Objekteigenschaft: Anzahl, Filterwert: 50, Operatoren: <, <=, =, >, >=, !=, Wertebereich)",
        example={},
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        additional_parameters=AdditionalProcessIOParameters(
            parameters=[
                Parameter(
                    name="kommonitorUiParams",
                    value=[{
                        "titleShort": "Anzahl Punkte in Polygon",
                        "apiName": "georesource_pointsInPolygon",
                        "dynamicLegend": "<b>Berechnung gem&auml;&szlig; Geodatenanalyse<br/><i>Anzahl Punkte des Datensatzes G<sub>1</sub> pro Raumeinheit</i> <br/> <i>Filterkriterium:</i> georesource_filter_legend <br/><br/>Legende zur Geodatenanalyse<br/>G<sub>1</sub>: ${georesourceSelection.datasetName}",
                        "calculation_info": "Summe aller Punkte innerhalb jedes Raumeinheits-Features.",
                        "optional_info": "Anwenden eines Filters anhand einer Objekteigenschaft",
                        "inputBoxes": [
                            {
                            "id": "georesource_id",
                            "title": "Benötigte punktbasierte Georessource",
                            "description": "",
                            "contents": [
                                "georesource_id"
                            ]
                            },
                            {
                            "id": "comp_filter",
                            "title": "Filter durch eine Objekteigenschaft (Optional)",
                            "description": "",
                            "contents": [
                                "comp_filter"
                            ]
                            }
                        ]
                        }]
                )
            ]
        ),
        inputs=KommonitorProcess.common_inputs | {
            "compGeoId": ProcessInput(
                id= "compGeoId",
                title="Auswahl der für die Berechnung erforderlichen Georesource",
                description="ID der Georesource.",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
            "comp_filter": ProcessInput(
                id="comp_filter",
                title="Filter durch eine Objekteigenschaft",
                description="",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    default={
                        "compFilterProp": "",
                        "compFilterOperator" : "",
                        "compFilterPropVal" : ""
                    }
                )
            )
        }, 
        outputs = KommonitorProcess.common_output
    )

    # run Method has to be implemented for all KomMonitor Skripts
    @staticmethod
    @task(cache_policy=NO_CACHE)
    def run(config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> Tuple[JobStatus, KommonitorResult, KommonitorJobSummary]:

        logger.debug("Starting execution...")

         # Load inputs
        inputs = config.inputs

        # Extract all relevant inputs
        target_id = inputs["target_indicator_id"]
        target_spatial_units = inputs["target_spatial_units"]
        target_time = inputs["target_time"]
        computation_georecources_id = inputs["compGeoId"]
        computation_filter_property = inputs["compFilterProp"]
        computation_filter_operator = inputs["compFilterOperator"]
        computation_filter_value = inputs["compFilterPropVal"]

        # Init object to store computation results
        result = KommonitorResult()
        job_summary = KommonitorJobSummary()

        try:
            # 3. Generate result || Main Script    
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            spatial_unit_controller = openapi_client.SpatialUnitsControllerApi(data_management_client)
            georesources_controller = openapi_client.GeorecourcesControllerApi(data_management_client)

            # create Indicator Objects and IndicatorCollection to store the informations belonging to the Indicator
            ti = IndicatorType(target_id, IndicatorCalculationType.TARGET_INDICATOR)
            
            # query indicator metadate to check for errors occured
            ti.get_indicator_by_id(indicators_controller)
            
            # extract all dates
            allDates = target_time["includeDates"]
            
            for spatial_unit in target_spatial_units:
                # check for existing allowedRoles for the concatenation of indicator and spatial unit
                allowedRoles = ti.check_su_allowedRoles(spatial_unit)
                
                # Init results and job summary for current spatial unit
                job_summary.init_spatial_unit_summary(spatial_unit)
                result.init_spatial_unit_result(spatial_unit, spatial_unit_controller, allowedRoles)
                
                # query data-management-api to get all spatial unit features for the current spatial unit.
                su_feature_collection = pykmhelper.get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit_controller, spatial_unit)

                # fetch the georesource feature collection
                georesource_collection = pykmhelper.get_all_georesource_features_by_id_without_preload_content(georesources_controller, computation_georecources_id)
                
                # apply the selected computation filter on the FeatureCollection
                if computation_filter_operator != "None":
                    georesource_collection = pykmhelper.applyComputationFilter_onFeatureCollection(georesource_collection, computation_filter_property, computation_filter_operator, computation_filter_value)

                # iterate over all features of the spatial unit an append the indicator
                indicator_values = []  

                for feature in su_feature_collection["features"]:
                    valueMapping = []
                    for targetTime in allDates:
                        try:
                            points_in_polygon = pykmhelper.pointsWithinPolygon(georesource_collection, feature)
                            collection_filtered_points = pykmhelper.filter_feature_lifespan(points_in_polygon, targetTime)
                            value = len(collection_filtered_points["features"])

                        except (RuntimeError, ZeroDivisionError) as r:
                            logger.error(r)
                            logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                            job_summary.add_processing_error("GEORESOURCE", computation_georecources_id, str(r), targetTime, feature["properties"]["ID"])
                            value = None

                        valueMapping.append({"indicatorValue": value, "timestamp": targetTime})

                    indicator_values.append({"spatialReferenceKey": feature["properties"]["ID"], "valueMapping": valueMapping})

                # Job Summary and results
                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates(allDates)
                job_summary.add_modified_resource(KOMMONITOR_DATA_MANAGEMENT_URL, target_id, spatial_unit)
                job_summary.complete_spatial_unit_summary()

                result.add_indicator_values(indicator_values)
                result.complete_spatial_unit_result()

                logger.info(result.values)
                logger.info(job_summary.summary)
            # 4.1 Return success and result
            return JobStatus.successful, result, job_summary
        except DataManagementException as e:
            # 4.2 Catch possible errors cleanly
            if e.spatial_unit and bool(job_summary):
                job_summary.add_data_management_api_error(e.resource_type, e.id, e.error_code, e)
                job_summary.complete_spatial_unit_summary()
            else:
                job_summary.init_spatial_unit_summary(target_spatial_units[0])
                job_summary.add_data_management_api_error(e.resource_type, e.id, e.error_code, e)
                job_summary.complete_spatial_unit_summary()    
            return JobStatus.failed, None, job_summary