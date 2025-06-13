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


@flow(persist_result=True, name="km_indicator_subtract", flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(KmIndicatorSubtract.run, job_id, execution_request)

class KmIndicatorSubtract(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_subtract",
        version="0.0.1",
        title="Subtraktion mehrerer Basisindikatoren von einem Referenzindikator",
        description= "Mindestens ein (Basis-)Indikator muss angegeben werden. Bei mehreren wird die Gesamtsumme der (Basis-)Indikatoren vom Wert des Referenzindikators abgezogen.",
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
                        "titleShort": "Multiplikation (beliebiger Indikatoren)",
                        "apiName": "indicator_division",
                        "formula": "$ dummy  $",
                        "legend": "<br/>$dummy$ ",
                        "dynamicLegend": "<br/> $dummy$",
                        "inputBoxes": [
                           {
                            "id": "dummy",
                            "title": "dummy",
                            "description": "dummy",
                            "contents": [
                                "dummy"
                            ]
                            }
                            
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
    @staticmethod
    @task(cache_policy=NO_CACHE)
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
            ti.get_indicator_by_id(indicators_controller)
            
            for indicator in collection.indicators:
                collection.indicators[indicator].get_indicator_by_id(indicators_controller)

            # calculate intersection dates and all dates that have to be computed according to target_time schema
            bool_missing_timestamp, all_times = pykmhelper.getAll_target_time_from_indicator_collection(ti, collection, target_time)   

            for spatial_unit in target_spatial_units:
                # check for existing allowedRoles for the concatenation of indicator and spatial unit
                allowedRoles = ti.check_su_allowedRoles(spatial_unit)
                
                # Init results and job summary for current spatial unit
                job_summary.init_spatial_unit_summary(spatial_unit)
                result.init_spatial_unit_result(spatial_unit, spatial_unit_controller, allowedRoles)
                
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
                    collection.indicators[indicator].get_indicator_by_spatial_unit_id_and_id_without_geometry(indicators_controller, spatial_unit)
                    
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
                            time_with_prefix = pykmhelper.getTargetDateWithPropertyPrefix(targetTime)
                            
                            compSum = 0
                            for indicator in collection.indicators:
                                if collection.indicators[indicator].type == IndicatorCalculationType.REFERENCE_INDICATOR:
                                    continue
                                compSum += float(collection.indicators[indicator].time_series[feature][time_with_prefix])

                            refValue = float(collection.indicators[reference_id].time_series[feature][time_with_prefix])

                            value = refValue - compSum
                        except (RuntimeError, TypeError) as r:
                            logger.error(r)
                            logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                            job_summary.add_processing_error("INDICATOR", reference_id, str(r), targetTime, feature)
                            value = None
    
                        valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
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