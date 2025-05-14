from typing import Dict, Optional
import logging
import math

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
# from ressources.PyKmHelper.pykmhelper import IndicatorCalculationType, IndicatorType, IndicatorCollection

class KmIndicatorPromille(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_promille",
        version="0.0.1",
        title="Promille Wert mehrerer Basisindikatoren von einem Referenzindikator",
        description= "Mindestens ein (Basis-)Indikator muss angegeben werden. Bei mehreren wird die Gesamtsumme der (Basis-)Indikatoren durch den Wert des Referenzindikators dividiert.",
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
                        "titleShort": "Promille-Wert (Quotient zwischen Basis-Indikatoren und einem Referenzindikator)",
                        "apiName": "indicator_promille",
                        "formula": "$$ \\frac{\\sum_{n=1}^{m} I_{n}}{I_{ref}} \\times 1000 $$",
                        "calculation_info": "Quotient zwischen (Basis-)Indikatoren und dem Referenzindikator multipliziert mit 1000",
                        "inputBoxes": [
                           {
                            "id": "reference_id",
                            "title": "Notwendiger Referenzindikator (Divisor)",
                            "description": "",
                            "contents": [
                                "reference_id"
                            ]
                            },
                            {
                            "id": "computation_ids",
                            "title": "Notwendige (Basis-)Indikatoren (Dividend)",
                            "description": "",
                            "contents": [
                                "computation_ids"
                            ]
                            },
                        ]
                    }]
                )
            ]
        ),
        inputs=KommonitorProcess.common_inputs | {
            "computation_ids": ProcessInput(
                id= "COMPUTATION_IDS",
                title="für die Berechnung erforderliche Basisindikatoren",
                description="Liste mit den Indikatoren-IDs der Basisindikatoren.",
                schema_=ProcessIOSchema(type_=ProcessIOType.ARRAY)
            ),
            "reference_id": ProcessInput(
                id= "REFERENCE_ID",
                title="für die Berechnung erforderlicher Referenzindikator",
                description="Divisor",
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
        computation_ids = inputs["computation_ids"]
        reference_id = inputs["reference_id"]
        target_spatial_units = inputs["target_spatial_units"]
        target_time = inputs["target_time"]
        
        
        # Init object to store computation results
        result = KommonitorResult()
        job_summary = KommonitorJobSummary()

        try:
            # 3. Generate result || Main Script    
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            spatial_unit_controller = openapi_client.SpatialUnitsControllerApi(data_management_client)

            # create Indicator Objects and IndicatorCollection to store the informations belonging to the Indicator
            ti = IndicatorType(target_id, IndicatorCalculationType.TARGET_INDICATOR)
            ri = IndicatorType(reference_id, IndicatorCalculationType.REFERENCE_INDICATOR)
            
            collection = IndicatorCollection()
            collection.add_indicator(ri)
            for indicator in computation_ids:
                collection.add_indicator(IndicatorType(indicator, IndicatorCalculationType.COMPUTATION_INDICATOR))
            
            # query indicator metadate to check for errors occured
            ti.meta = indicators_controller.get_indicator_by_id(
                target_id)
            
            for indicator in collection.indicators:
                collection.indicators[indicator].meta = indicators_controller.get_indicator_by_id(
                indicator)

            # calculate intersection dates and all dates that have to be computed according to target_time schema
            bool_missing_timestamp, all_times = pykmhelper.getAll_target_time_from_indicator_collection(ti, collection, target_time)   

            for spatial_unit in target_spatial_units:
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(spatial_unit)
                job_summary.init_spatial_unit_summary(spatial_unit)

                # query data-management-api to get all spatial unit features for the current spatial unit.
                # store the list containing all features-IDs as an attribute for the collection
                collection.fetch_all_spatial_unit_features(spatial_unit_controller, spatial_unit)

                # catch missing timestamp error
                if bool_missing_timestamp:
                     collection.check_applicable_target_dates(job_summary)

                # catch missing spatial unit error
                collection.check_applicable_spatial_units(spatial_unit, job_summary)

                # query the correct indicator for numerator and denominator
                for indicator in collection.indicators:
                    collection.indicators[indicator].values = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                        indicator, 
                        spatial_unit)
                    
                collection.fetch_indicator_feature_time_series()

                # get the intersection of all applicable su_features and check for missing spatial unit feature error
                collection.find_intersection_applicable_su_features()
                collection.check_applicable_spatial_unit_features(job_summary)

                logger.debug("Retrieved required indicators successfully")

                # iterate over all features an append the indicator here happen the main calculations for the requested values
                indicator_values = []  
                
                for feature in collection.intersection_su_features:
                    valueMapping = []
                    for targetTime in all_times:
                        try:
                            try:
                                time_with_prefix = pykmhelper.getTargetDateWithPropertyPrefix(targetTime)
                            
                                compSum = 0
                                for indicator in collection.indicators:
                                    if collection.indicators[indicator].type == IndicatorCalculationType.REFERENCE_INDICATOR:
                                        continue
                                    compSum += float(collection.indicators[indicator].time_series[feature][time_with_prefix])

                                refValue = float(collection.indicators[reference_id].time_series[feature][time_with_prefix])

                                value = compSum / refValue * 1000
                            except TypeError:
                                value = None
                                
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        except RuntimeError as r:
                            logger.error(r)
                            logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                            job_summary.add_processing_error("INDICATOR", reference_id, str(r))
    
                    indicator_values.append({"spatialReferenceKey": feature, "valueMapping": valueMapping})
                
                # Job Summary and results
                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates(all_times)
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