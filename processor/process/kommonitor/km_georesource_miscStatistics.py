import logging
from typing import Tuple
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


@flow(persist_result=True, name="km_georesource_miscStatistics", flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(KmGeoresourceMiscStatistics.run, job_id, execution_request)

class KmGeoresourceMiscStatistics(KommonitorProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id="km_georesource_miscStatistics",
        version="0.0.1",
        title="Statistiken anhand Eigenschaft der punktbasierten Georessource",
        description= "Auswahl einer punktbasierten Georessource, für die anhand einer bestimmten Eigenschaft und Auswahl einer statistischen Methode Indikatoren-Kennwerte pro Raumeinheit zu enthalten.",
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
                        "apiName": "georesource_miscStatistics",
                        "dynamicLegend": "<b>Geodatenanalyse: Statistische Berechnung <i>´${compMeth}´ anhand Objekteigenschaft ´${compProp}´</i> f&uuml;r alle Punktobjekte des Datensatzes G<sub>1</sub> innerhalb des jeweiligen Raumeinheits-Features</i><b><br/><br/>Legende zur Geodatenanalyse</b><br/>G<sub>1</sub>: ${georesourceSelection.datasetName}",
                        "calculation_info": "Identifikation aller Punkte innerhalb jedes Raumeinheits-Features mit anschließender statistischen Indikatorenberechnung anhand gew&auml;hlter Objekt-Eigenschaft",
                        "inputBoxes": [
                            {
                            "id": "georesource_id",
                            "title": "Benötigte punkthafte Georessource",
                            "description": "",
                            "contents": [
                                "georesource_id"
                            ]
                            },
                            {
                            "id": "compProp",
                            "title": "Notwendige Objekt-Eigenschaft",
                            "description": "",
                            "contents": [
                                "compProp"
                            ]
                            },
                            {
                            "id": "comp_meth",
                            "title": "Notwendige statistische Berechnungsmethode",
                            "description": "Auswahl der statistischen Berechnungsmethode",
                            "contents": [
                                "compMeth"
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
            "compProp": ProcessInput(
                id= "compProp",
                title="Numerische Objekteigenschaft.",
                description="Auswahl der für die Berechnung erforderlichen Eigenschaft.",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
            "compMeth": ProcessInput(
                id= "compMeth",
                title="Auswahl der statistischen Berechnungsmethode",
                description="",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    enum=[
                        {
                            "apiName": "MIN",
                            "displayName": "Minimum",
                        },
                        {
                            "apiName": "MAX",
                            "displayName": "Maximum",
                        },
                        {
                            "apiName": "MEAN",
                            "displayName": "Arithmetisches Mittel",
                        },
                        {
                            "apiName": "MEDIAN",
                            "displayName": "Median",
                        },
                        {
                            "apiName": "SUM",
                            "displayName": "Summe",
                        },
                        {
                            "apiName": "STANDARD_DEVIATION",
                            "displayName": "Standardabweichung",
                        }
                    ],                    
                    default={
                        "apiName": "MIN",
                        "displayName": "Minimum",
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
        computation_property = inputs["compProp"]
        computation_method = inputs["compMeth"]

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
            ti.meta = indicators_controller.get_indicator_by_id(
                target_id)
            
            # extract all dates
            allDates = target_time["includeDates"]
            
            for spatial_unit in target_spatial_units:
                # check for existing allowedRoles for the concatenation of indicator and spatial unit
                allowedRoles = ti.check_su_allowedRoles(spatial_unit)
                
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(spatial_unit, spatial_unit_controller, allowedRoles)
                job_summary.init_spatial_unit_summary(spatial_unit)

                # query data-management-api to get all spatial unit features for the current spatial unit.
                su_feature_collection = pykmhelper.get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit_controller, spatial_unit)

                # fetch the georesource feature collection
                georesource_collection = pykmhelper.get_all_georesource_features_by_id_without_preload_content(georesources_controller, computation_georecources_id)
                
                # iterate over all features of the spatial unit an append the indicator
                indicator_values = []  


                for feature in su_feature_collection["features"]:
                    valueMapping = []
                    for targetTime in allDates:
                        try:
                            points_in_polygon = pykmhelper.pointsWithinPolygon(georesource_collection, feature)
                            filtered_points = pykmhelper.filter_feature_lifespan(points_in_polygon, targetTime)
                            propertyValueArray = pykmhelper.getPropertyValueArray(filtered_points, computation_property)
                            value = pykmhelper.applyComputationMethod(propertyValueArray, computation_method)

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