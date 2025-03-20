from typing import Dict, Optional
import logging

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi.process.base import *
from processor.process.base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from pygeoapi.util import JobStatus

from ressources.PyKmHelper import pykmhelper

class km_indicator_divide(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_divide",
        version="0.0.1",
        title="Division of two different Indicators.",
        example={},
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs=KommonitorProcess.common_inputs | {
            "reference_id": ProcessInput(
                title="reference_id",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
            "computation_ids": ProcessInput(
                title="computation_ids",
                schema_= ProcessIOSchema(type_=ProcessIOType.ARRAY, items=ProcessIOSchema(type_=ProcessIOType.STRING))
            )
        },
        outputs = KommonitorProcess.common_output
    )

    # run Method has to be implemented for all KomMonitor Skripts
    @staticmethod
    def run(self,
            config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> (JobStatus, Dict):

        logger.debug("Starting execution...")

         # Load inputs
        inputs = config.inputs
        # Extract all relevant inputs
        target_indicator_id = inputs["target_indicator_id"]
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

            # query indicator metadate to check for errors occured
            all_computation_indicator_meta = []
            for indicator in computation_ids:
                all_computation_indicator_meta.append(indicators_controller.get_indicator_by_id(indicator))
            
            target_indicator_metadata = indicators_controller.get_indicator_by_id(
                target_indicator_id)
            
            all_computation_applicable_dates = [set(indicator["applicableDates"]) for indicator in all_computation_indicator_meta]
            
            target_indicator_applicable_dates = target_indicator_metadata["applicableDates"]

            all_computation_spatial_units = []
            for indicator in all_computation_indicator_meta:
                temp = []
                for unit in indicator["applicableSpatialUnit"]:
                    temp.append(unit["spatialUnitID"])
                all_computation_spatial_units.append(temp)

            all_times = pykmhelper.getAll_target_time(target_time, set(target_indicator_applicable_dates), all_computation_applicable_dates)

            for spatial_unit in target_spatial_units:
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(spatial_unit)
                job_summary.init_spatial_unit_summary(spatial_unit)

                # catch missing timestamp error
                for indicator in all_computation_applicable_dates:
                    missing_dates = [date for date in indicator if not date in all_times and not date in missing_dates]
                
                if len(missing_dates) >= 1:
                    job_summary.add_missing_timestamp_error("INDICATOR", computation_indicator_id, missing_dates)  
                
                # catch missing spatial unit error
                if not spatial_unit in computation_indicator_applicable_spatial_units:
                    job_summary.add_missing_spatial_unit_error(computation_indicator_id)

                # catch missing spatial unit feature error
                """
                Endpoint of spatial unit controller api has to be implemented
                """
                # query the correct reference indicator
                reference_indicator = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                        reference_id, 
                        spatial_unit)
                
                logger.debug("Retrieved required reference indicator successfully")

                for indicator_id in computation_ids:
                    # query the correct indicator 
                    computation_indicator = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                        indicator_id, 
                        spatial_unit)
                    
                    logger.debug(f"Retrieved required computation indicator with id: '{indicator_id}' successfully...")

                    # iterate over all features an append the indicator
                    indicator_values = []  
                    for indicator_feature in computation_indicator:
                        valueMapping = []
                        # find correct spatial unit feature in reference indicator
                        for reference_feature in reference_indicator:
                            if indicator_feature["ID"] == reference_indicator["ID"]:
                                break
                        
                        for targetTime in all_times:
                            time_with_prefix = pykmhelper.getTargetDateWithPropertyPrefix(targetTime)
                            value = float(indicator_feature[time_with_prefix]) / float(reference_feature[time_with_prefix])
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        spatialReferenceKey = indicator_feature["ID"]
                        indicator_values.append({"spatialReferenceKey": spatialReferenceKey, "valueMapping": valueMapping})

                # Job Summary and results
                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates(all_times)
                job_summary.add_modified_resource(KOMMONITOR_DATA_MANAGEMENT_URL, target_indicator_id, spatial_unit)
                job_summary.complete_spatial_unit_summary()

                result.add_indicator_values(indicator_values)
                result.complete_spatial_unit_result()
                 
            # 4.1 Return success and result
            return JobStatus.successful, result, job_summary
        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            return JobStatus.failed, None