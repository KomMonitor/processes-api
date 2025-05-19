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
from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from pygeoapi.util import JobStatus

from .. import pykmhelper
from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
# from ....ressources.PyKmHelper.pykmhelper import IndicatorCalculationType, IndicatorType, IndicatorCollection

class KmGeoresourceLengthLineSegmentsWithinPolygon(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_georesource_length_lineSegmentsWithinPolygon",
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
                title="Auswahl der für die Berechnung erforderlichen Linienhaften Georesource",
                description="ID der Georesource.",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
            "compFilterProp": ProcessInput(
                id= "compFilterProp",
                title="Objekteigenschaft.",
                description="Auswahl der für die Berechnung erforderlichen Eigenschaft.",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING, default=None),
            ),
            "compFilterOperator": ProcessInput(
                id= "compFilterOperator",
                title="Operator der Filteroption",
                description="Zu verwendender Operator für die Objektfilterung",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    enum=[
                        {
                            "apiName": "Equal",
                            "displayName": "Gleich"
                        },
                        {
                            "apiName": "Greater_than",
                            "displayName": "Groeßer als"
                        },
                        {
                            "apiName": "Greater_than_or_equal",
                            "displayName": "Groeßer als oder gleich"
                        },
                        {
                            "apiName": "Less_than",
                            "displayName": "Kleiner als"
                        },
                        {
                            "apiName": "Less_than_or_equal",
                            "displayName": "Kleiner als oder gleich"
                        },
                        {
                            "apiName": "Unequal",
                            "displayName": "Ungleich"
                        },
                        {
                            "apiName": "Contains",
                            "displayName": "Enthaelt (Komma separierte Liste)"
                        },
                        {
                            "apiName": "Range",
                            "displayName": "Innerhalb"
                        },
                        {
                            "apiName": "None",
                            "displayName": "Ungefiltert"
                        }
                    ],
                    default={
                        "apiName": "None",
                        "displayName": "Ungefiltert"
                    }
                )
            ),
            "compFilterPropVal": ProcessInput(
                id= "compFilterPropVal",
                title="Filterwert",
                description="Wert nach dem die Objekte gefiltert werden sollen",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING, default=None)
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
                response_data = spatial_unit_controller.get_all_spatial_unit_features_by_id_without_preload_content(spatial_unit)
                su_feature_collection = json.loads(response_data.data)

                # fetch the georesource feature collection
                georesource = georesources_controller.get_all_georesource_features_by_id_without_preload_content(computation_georecources_id)
                georesource_collection = json.loads(georesource.data)

                # apply the selected computation filter on the FeatureCollection
                if computation_filter_operator != "None":
                    georesource_collection = pykmhelper.applyComputationFilter_onFeatureCollection(georesource_collection, computation_filter_property, computation_filter_operator, computation_filter_value)

                georesource_collection = pykmhelper.transformMultiLineStringToLineStrings(georesource_collection)
                
                # iterate over all features of the spatial unit an append the indicator
                indicator_values = []  

                for feature in su_feature_collection["features"]:
                    valueMapping = []
                    for targetTime in allDates:
                        try:
                            lines_in_polygon = pykmhelper.intersectLineFeatureCollectionByPolygonFeature(georesource_collection, feature)
                            collection_filtered_lines = pykmhelper.filter_feature_lifespan(lines_in_polygon, targetTime)
                            
                            value = pykmhelper.summarizeLineSegmentLenghts(collection_filtered_lines)

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
        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            return JobStatus.failed, None