import json
from typing import Dict, Optional
import logging

import openapi_client
from IPython.core.events import pre_run_cell
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi.process.base import *
from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, DataManagementException

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from pygeoapi.util import JobStatus

from .. import pykmhelper
from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
# from ....ressources.PyKmHelper.pykmhelper import IndicatorCalculationType, IndicatorType, IndicatorCollection

class KmGeoresourceMiscStatistics(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_georesource_miscStatistics",
        version="0.0.1",
        title="Division zweier Indikatoren",
        description= "Berechnet den Wert eines Indikators geteilt durch einen Weiteren.",
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
                        "titleShort": "Division (Quotient zweier Indikatoren)",
                        "apiName": "indicator_division",
                        "formula": "$ \\frac{I_{1}}{I_{2}}  $",
                        "legend": "<br/>$I_{1}$ = Dividend-Indikator <br/>$I_{2}$ = Divisor-Indikator ",
                        "dynamicLegend": "<br/> $I_{1}$: ${refIndicatorSelection.indicatorName} [ ${refIndicatorSelection.unit} ] <br/> $I_{2}$: ${compIndicatorSelection.indicatorName} [ ${compIndicatorSelection.unit} ]",
                        "inputBoxes": [
                           {
                            "id": "reference_id",
                            "title": "Notwendiger Dividend-Indikator",
                            "description": "",
                            "contents": [
                                "reference_id"
                            ]
                            },
                            {
                            "id": "computation_id",
                            "title": "Notwendiger Divisor-Indikator",
                            "description": "",
                            "contents": [
                                "computation_id"
                            ]
                            },
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
                description="Zu verwendende statistische Berechnungsmethode",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            )
        }, 
        outputs = KommonitorProcess.common_output
    )

    # run Method has to be implemented for all KomMonitor Skripts
    def run(self,
            config: KommonitorProcessConfig,
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

                print(result.values)
                print(job_summary.summary)
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