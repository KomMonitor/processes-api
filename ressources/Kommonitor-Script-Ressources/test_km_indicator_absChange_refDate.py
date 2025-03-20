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

class km_indicator_absChange_refDate(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_absChange_refDate",
        version="0.0.1",
        title="Absolute change of an indicator compared to the reference date.",
        example={},
        job_control_options=[
            ProcessJobControlOption.SYNC_EXECUTE,
            ProcessJobControlOption.ASYNC_EXECUTE,
        ],
        inputs=KommonitorProcess.common_inputs | {
            "reference_date": ProcessInput(
                title="reference_date",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING, default=None)
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
        computation_indicator_id = inputs["computation_id"]
        target_spatial_units = inputs["target_spatial_units"]
        target_time = inputs["target_time"]
        reference_date = inputs["reference_date"]

        # Init object to store computation results
        result = KommonitorResult()
        job_summary = KommonitorJobSummary()

        try:
            # 3. Generate result || Main Script    
            indicators_controller = openapi_client.IndicatorsControllerApi(data_management_client)
            spatial_unit_controller = openapi_client.SpatialUnitsControllerApi(data_management_client)

            # query indicator metadate to check for errors occured
            computation_indicator_metadata = indicators_controller.get_indicator_by_id(
                computation_indicator_id)
            
            target_indicator_metadata = indicators_controller.get_indicator_by_id(
                target_indicator_id)
            
            computation_indicator_applicable_dates = computation_indicator_metadata["applicableDates"]
            target_indicator_applicable_dates = target_indicator_metadata["applicableDates"]

            computation_indicator_applicable_spatial_units = []
            for unit in computation_indicator_metadata["applicableSpatialUnit"]:
                computation_indicator_applicable_spatial_units.append(unit["spatialUnitID"])

            all_times = pykmhelper.getAll_target_time(target_time, set(target_indicator_applicable_dates), [set(computation_indicator_applicable_dates)])

            for spatial_unit in target_spatial_units:
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(spatial_unit)
                job_summary.init_spatial_unit_summary(spatial_unit)

                 # catch missing timestamp error
                missing_dates = [date for date in computation_indicator_applicable_dates if not date in all_times]
                if len(missing_dates) >= 1:
                    job_summary.add_missing_timestamp_error("INDICATOR", computation_indicator_id, missing_dates)  
                
                # catch missing spatial unit error
                if not spatial_unit in computation_indicator_applicable_spatial_units:
                    job_summary.add_missing_spatial_unit_error(computation_indicator_id)

                # catch missing spatial unit feature error
                """
                Endpoint of spatial unit controller api has to be implemented
                """

                # query the correct indicator 
                computation_indicator = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                    computation_indicator_id, 
                    spatial_unit)
                
                logger.debug("Retrieved required computation indicator successfully...")
                
                # iterate over all features an append the indicator
                indicator_values = []  
                for feature in computation_indicator["features"]:
                    valueMapping = []
                    for target_time in all_times:
                        value = pykmhelper.changeAbsolute_referenceDate(feature, target_time, reference_date)
                        valueMapping.append({"indicatorValue": value, "timestamp": target_time})
                    
                    spatialReferenceKey = feature["properties"]["ID"]
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