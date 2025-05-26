import math

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from prefect import task, flow
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus
from pygeoapi_prefect import schemas
from pygeoapi_prefect.schemas import ProcessDescription, ProcessJobControlOption, Parameter, \
    AdditionalProcessIOParameters
from pygeoapi_prefect.schemas import ProcessInput, ProcessIOSchema, ProcessIOType

try:
    from .. import pykmhelper
except ImportError:
    from processor.process import pykmhelper

try:
    from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
except ImportError:
    from processor.process.pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType

try:
    from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL
except ImportError:
    from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL


@flow(persist_result=True)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    KommonitorProcess.execute_process_flow(KmIndicatorMultiply.run, job_id, execution_request)


class KmIndicatorMultiply(KommonitorProcess):
    process_flow = process_flow

    detailed_process_description = ProcessDescription(
        id="km_indicator_multiply",
        version="0.0.1",
        title="Multiplikation beliebig vieler Indikatoren",
        description= "Berechnet den Wert welcher durch Multiplikation beliebig vieler Indikatoren entsteht.",
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
                        "apiName": "indicator_multiplication",
                        "calculation_info": "Produkt aller (Basis-)Indikatoren",
                        "formula": "$ \\prod_{n=1}^{m} I_{n} $",
                        "legend": "",
                        "dynamicFormula": "$$ prod_baseIndicators $$",
                        "dynamicLegend": "${list_baseIndicators}",
                        "inputBoxes": [
                            {
                                "id": "computation_ids",
                                "title": "Notwendige (Basis-)Indikatoren (Faktoren)",
                                "description": "",
                                "contents": [
                                    "computation_ids"
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
                schema_=ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING))
            )
        }, 
        outputs = KommonitorProcess.common_output
    )

    # run Method has to be implemented for all KomMonitor Skripts
    @task
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
            
            collection = IndicatorCollection()
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
                result.init_spatial_unit_result(spatial_unit, spatial_unit_controller)
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
                                
                                allIndicatorValues = []
                                for indicator in collection.indicators:
                                    allIndicatorValues.append(float(collection.indicators[indicator].time_series[feature][time_with_prefix]))
                                
                                value = math.prod(allIndicatorValues)
                            except TypeError:
                                value = None    
                            
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        except RuntimeError as r:
                            logger.error(r)
                            logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                            job_summary.add_processing_error("INDICATOR", computation_ids[0], str(r), targetTime, feature)
    
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

