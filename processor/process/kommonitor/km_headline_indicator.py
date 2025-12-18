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
    from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name, Popularity
except ImportError:
    from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, DataManagementException, \
        KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL, generate_flow_run_name, Popularity

try:
    from .. import pykmhelper
except ImportError:
    from processor.process import pykmhelper
    
try:
    from ..pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType
except ImportError:
    from processor.process.pykmhelper import IndicatorType, IndicatorCollection, IndicatorCalculationType



# this name should be set for @flow(name='<processName>') and within detailed_process_description as 
# additional_parameters.parameters[0].value[0].apiName
# this is necessary in order to have a comparable name between prefect schedules and pygeoAPI process descriptions
processName = "km_headline_indicator"

@flow(persist_result=True, name=processName, flow_run_name=generate_flow_run_name)
def process_flow(
        job_id: str,
        execution_request: schemas.ExecuteRequest
) -> dict:
    return KommonitorProcess.execute_process_flow(KmHeadlineIndicator.run, job_id, execution_request)

class KmHeadlineIndicator(KommonitorProcess):
    process_flow = process_flow
    
    detailed_process_description = ProcessDescription(
        id=processName,
        version="0.0.1",
        title="Leitindikator",
        description= "Berechnet einen neuen Leitindikator aus beliebig vielen Basisindikatoren.",
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
                        "longTitle": "Leitindikator - verkettete Berechnung",
                        "apiName": processName,
                        "formula": "$ \\frac{I_{1}}{I_{2}}  $",
                        "legend": "<br/>$I_{1}$ = Dividend-Indikator <br/>$I_{2}$ = Divisor-Indikator ",
                        "dynamicLegend": "<br/> $I_{1}$: ${refIndicatorSelection.indicatorName} [ ${refIndicatorSelection.unit} ] <br/> $I_{2}$: ${compIndicatorSelection.indicatorName} [ ${compIndicatorSelection.unit} ]",
                        "inputBoxes": [
                           {
                                "id": "computation_ids",
                                "title": "Notwendige (Basis-)Indikatoren mit dazugehöriger Popularität",
                                "description": "",
                                "contents": [
                                    "computation_ids"
                                ]
                           },
                           {
                                "id": "computation_method",
                                "title": "Art der Normierung (Min/Max oder Z-Wert)",
                                "description": "",
                                "contents": [
                                    "computation_method"
                                ]
                           },
                           {
                                "id": "aggregation_method",
                                "title": "Notwendige statistische Aggregationsmethode",
                                "description": "",
                                "contents": [
                                    "aggregation_method"
                                ]
                           }
                        ]
                    }]
                )
            ]
        ),
        inputs=KommonitorProcess.common_inputs | {
            "computation_ids": ProcessInput(
                id="COMPUTATION_IDS",
                title="für die Berechnung erforderliche Basisindikatoren",
                description="Liste mit den Indikatoren-IDs der Basisindikatoren mit deren Popularitätseinstellung.",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.ARRAY,
                    items=ProcessIOSchema(
                        type_=ProcessIOType.OBJECT,
                        properties={
                            "ID": ProcessIOSchema(type_=ProcessIOType.STRING, title="Indikator-ID"),
                            "POPULARITY": ProcessIOSchema(
                                type_=ProcessIOType.STRING,
                                title="Popularität für die Normierung (normal oder invers)",
                                enum=[Popularity.INVERT, Popularity.NORMAL]
                            )
                        },
                        required=["ID", "POPULARITY"]
                    )
                )
            ),
            "aggregation_method": ProcessInput(
                id= "AGGREGATION_METHOD",
                title="Auswahl der angewandten statistischen Aggregationsmethode der Basisindikatoren.",
                description="",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    enum=[
                        {
                            "apiName": "MIN",
                            "displayName": "Minimum",
                        },
                        {
                            "apiName": "MEAN",
                            "displayName": "Arithmetisches Mittel",
                        },
                        {
                            "apiName": "GEOMEAN",
                            "displayName": "Geometrisches Mittel",
                        }
                    ],                    
                    default={
                        "apiName": "MEAN",
                        "displayName": "Arithmetisches Mittel",
                    }
                )
            ),
            "computation_method": ProcessInput(
                id= "COMPUTATION_METHOD",
                title="Art der Normalisierung (Ranked Min/Max, Z-Wert)",
                description="",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    enum=[
                        {
                            "apiName": "RANKEDMINMAX",
                            "displayName": "normal ([value - min] / [max - min])",
                        },
                        {
                            "apiName": "ZSCORE",
                            "displayName": "z = (x - mean) / stdev",
                        }
                    ],                    
                    default={
                        "apiName": "RANKEDMINMAX",
                        "displayName": "normal ([value - min] / [max - min])",
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
        computation_ids = inputs["computation_ids"]
        aggregation_method = inputs["aggregation_method"]
        computation_method = inputs["computation_method"]
        
        # Init object to store computation results
        result = KommonitorResult()
        job_summary = KommonitorJobSummary()

        try:
            # 3. Generate result || Main Script    
            indicators_controller = openapi_client.IndicatorsApi(data_management_client)
            spatial_unit_controller = openapi_client.SpatialUnitsApi(data_management_client)

            # create Indicator Objects and IndicatorCollection to store the informations belonging to the Indicator
            ti = IndicatorType(target_id, IndicatorCalculationType.TARGET_INDICATOR)
            
            collection = IndicatorCollection()
            for indicator in computation_ids:
                collection.add_indicator(IndicatorType(indicator["ID"], IndicatorCalculationType.COMPUTATION_INDICATOR))
                collection.indicators[indicator["ID"]].method = indicator["POPULARITY"]
                
            # query indicator metadate to check for errors occured
            # ti.meta = indicators_controller.get_indicator_by_id(
            #    target_id)
            ti.get_indicator_by_id(indicators_controller)
            
            print(ti.meta)
            for indicator in collection.indicators:
                collection.indicators[indicator].get_indicator_by_id(indicators_controller)
                    
            # calculate intersection dates and all dates that have to be computed according to target_time schema
            bool_missing_timestamp, all_times = pykmhelper.getAll_target_time_from_indicator_collection(ti, collection, target_time)   

            for spatial_unit in target_spatial_units:
                # Init results and job summary for current spatial unit
                job_summary.init_spatial_unit_summary(spatial_unit)
                result.init_spatial_unit_result_with_indicator(spatial_unit, spatial_unit_controller, ti)

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

                # find the functions for requested normalization and aggregation
                if aggregation_method == "MEAN":
                    agg_func = pykmhelper.mean
                elif aggregation_method == "GEOMEAN":
                    agg_func = pykmhelper.geomean
                elif aggregation_method == "MIN":
                    agg_func = pykmhelper.min
                else:
                    raise DataManagementException("The aggregation method is not in the list of allowed values.", computation_ids[0]["ID"], "INDICATOR", 500)

                         
                if computation_method == "RANKEDMINMAX":
                    z_score = False
                    normal = pykmhelper.minMaxNormalization_wholeValueArray
                    invert = pykmhelper.minMaxNormalization_wholeValueArray_inverted
                    
                elif computation_method == "ZSCORE":
                    z_score = True
                    normal = pykmhelper.zScore_normalization_wholeValueArray       
                    invert = pykmhelper.zScore_normalization_wholeValueArray_inverted
                else:
                    raise DataManagementException("The computation method is not in the list of allowed values.", computation_ids[0]["ID"], "INDICATOR", 500)
                    
                collection.search_nan_features(all_times)

                for indicator_id, indicator_obj in collection.indicators.items():
                    indicator_obj.lists = {}
                    if indicator_obj.method == "NORMAL":
                        func = normal
                    elif indicator_obj.method == "INVERT":
                        func = invert
                        
                    for raw_time in all_times:
                        time_key = pykmhelper.getTargetDateWithPropertyPrefix(raw_time)
                        indicator_obj.lists[time_key] = []
                        for feature in collection.intersection_su_features:
                            if not feature in collection.nan_features[time_key]:
                                feature_series = indicator_obj.time_series.get(feature, {})
                                value = feature_series.get(time_key)
                                indicator_obj.lists[time_key].append(value)

                        if not z_score:
                            ranked = pykmhelper.rank(indicator_obj.lists[time_key])
                            normalized = func(ranked)
                        else:
                            normalized = func(indicator_obj.lists[time_key])
                            
                        indicator_obj.lists[time_key] = normalized


                # iterate over all features and append the indicator
                y = 0
                indicator_values = []
                for i, feature in enumerate(collection.intersection_su_features):
                    valueMapping = []
                    for targetTime in all_times:
                        try:
                            time_key = pykmhelper.getTargetDateWithPropertyPrefix(targetTime)
                            if feature in collection.nan_features[time_key]:
                                y += 1
                                raise RuntimeError("In one of the indicators, the spatial unit does not have a valid numerical value — calculation not possible.")

                            try:
                                value_list = []
                                for indicator_id, indicator_obj in collection.indicators.items():
                                    value_list.append(indicator_obj.lists[time_key][i - y])
                                    
                                value = agg_func(value_list)
                            except TypeError:
                                value = None
                                
                        except (RuntimeError, ZeroDivisionError, TypeError) as r:
                            logger.error(r)
                            logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                            job_summary.add_processing_error("INDICATOR", indicator_id, str(r), targetTime, feature)
                            value = None
                        
                        valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                    indicator_values.append({"spatialReferenceKey": str(feature), "valueMapping": valueMapping})
                
                # Job Summary and results
                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates(all_times)
                job_summary.add_modified_resource(KOMMONITOR_DATA_MANAGEMENT_URL, target_id, spatial_unit)
                job_summary.complete_spatial_unit_summary()

                result.add_indicator_values(indicator_values)
                result.complete_spatial_unit_result()

                # logger.info(result.values)
                # logger.info(job_summary.summary)
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