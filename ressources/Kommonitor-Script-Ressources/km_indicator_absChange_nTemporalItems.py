from typing import Dict, Optional

from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from processor.process.base import KommonitorProcess, KommonitorProcessConfig
from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput

from ressources.PyKmHelper import pykmhelper

class km_indicator_absChange_nTemporalItems(KommonitorProcess):
    # TODO create process description for the script the following description is for hello-world example
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""

                    Process Description

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    

    # run Method has to be implemented for all KomMonitor Skripts
    @staticmethod
    def run(config: KommonitorProcessConfig,
            logger: logging.Logger,
            data_management_client: ApiClient) -> (JobStatus, Optional[Dict[str, OutputExecutionResultInternal]]):

        # 1. Load inputs
        inputs = config.inputs

        # 2. Log some useful stuff
        logger.debug("Starting execution...")

        try:
            # 3. Generate result || Main Script    
            results = []
            jobSummary = []

            for spatialUnit in inputs["target_spatial_unit"]:

                georesources_controller = openapi_client.IndicatorsControllerApi(data_management_client)
                
                # query the correct indicator and get all target_times needed
                computationIndicator = georesources_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                    inputs["computation_id"], 
                    inputs[spatialUnit])
                
                logger.debug("Retrieved required computation indicator successfully...")

                allTimes = pykmhelper.getAll_target_time(inputs["target_time"], computationIndicator)
                temporalItems = inputs["number_of_temporal_items"]
                
                if inputs["temporal_type"] == "YEARS":
                    indicatorValues = []
                    for feature in computationIndicator["features"]:
                        valueMapping = []
                        for targetTime in allTimes:
                            value = pykmhelper.changeAbsolute_n_years(feature, targetTime)
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        spatialReferenceKey = feature["properties"]["ID"]
                        indicatorValues.append({"spatialReferenceKey": spatialReferenceKey, "valueMapping": valueMapping})

                elif inputs["temporal_type"] == "MONTHS":
                    indicatorValues = []
                    for feature in computationIndicator["features"]:
                        valueMapping = []
                        for targetTime in allTimes:
                            value = pykmhelper.changeAbsolute_n_months(feature, targetTime)
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        spatialReferenceKey = feature["properties"]["ID"]
                        indicatorValues.append({"spatialReferenceKey": spatialReferenceKey, "valueMapping": valueMapping})

                elif inputs["temporal_type"] == "DAYS":
                    indicatorValues = []
                    for feature in computationIndicator["features"]:
                        valueMapping = []
                        for targetTime in allTimes:
                            value = pykmhelper.changeAbsolute_n_days(feature, targetTime)
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        spatialReferenceKey = feature["properties"]["ID"]
                        indicatorValues.append({"spatialReferenceKey": spatialReferenceKey, "valueMapping": valueMapping})

                results.append({"applicableSpatialUnit": spatialUnit, "indicatorValues": indicatorValues})
                        
                       

            # 4.1 Return success and result
            return JobStatus.successful, {"results": results}
        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            return JobStatus.failed, None