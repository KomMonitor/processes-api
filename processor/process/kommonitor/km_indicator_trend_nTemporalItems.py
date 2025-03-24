from typing import Dict, Optional
import logging

import openapi_client
from openapi_client import ApiClient
from openapi_client.rest import ApiException
from pygeoapi.process.base import *
from pygeoapi.util import JobStatus

from pygeoapi.process.base import *
from ..base import KommonitorProcess, KommonitorProcessConfig, KommonitorResult, KommonitorJobSummary, KOMMONITOR_DATA_MANAGEMENT_URL

from pygeoapi_prefect.schemas import ProcessInput, ProcessDescription, ProcessIOType, ProcessIOSchema, ProcessJobControlOption, Parameter, AdditionalProcessIOParameters, OutputExecutionResultInternal, ProcessOutput
from pygeoapi.util import JobStatus

from ..pykmhelper import *

class KmIndicatorTrendNTemporalItems(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_Trend_nTemporalItems",
        version="0.0.1",
        title="Trendberechnung bezogen auf Zeitspanne",
        description= "Berechnet den Trend über eine vergangene Zeitspanne eines Indikators als Steigung b der Geraden bei einer linearen Regression im Verhältnis zum Indikatorwert des ersten Jahres.",
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
                        "titleShort": "Trendberechnung (mittels linearer Regression)",
                        "apiName": "indicator_trend",
                        "formula": "$$ T = 100 \times \frac{b}{I_{1}} $$ wobei $$ b = \frac{\sum_{n=1}^{m}((A_{n} - \bar{A}) \times (I_{n} - \bar{I}))}{\sum_{n=1}^{m} (A_{n} - \bar{A})^2} $$",
                        "legend": "<br/>$T$ = Trend<br/>$m$ = Anzahl konsekutiver vergangener Tage/Monate/Jahre <br/>$A_{n}$ = aufeinander folgende Jahre<br/>$\bar{A}$ = arithmetisches Mittel der aufeinander folgenden Jahre<br/>$I_{n}$ = Indikatorenwerte der aufeinander folgenden Jahre<br/>$\bar{I}$ = arithmetisches Mittel der Indikatorenwerte der aufeinander folgenden Jahre",
                        "dynamicLegend": "<br/>$T$ = Trend<br/>$m$ = ${number_of_temporal_items} konsekutiver vergangener ${temporal_type} <br/>$A_{n}$ = aufeinander folgende ${temporal_type}<br/>$\bar{A}$ = arithmetisches Mittel der aufeinander folgenden ${temporal_type}<br/>$I_{n}$ = Indikatorenwerte der aufeinander folgenden ${temporal_type}<br/>$\bar{I}$ = arithmetisches Mittel der Indikatorenwerte der aufeinander folgenden ${temporal_type} <br/> $I$ = Indikator '${computation_id_name} ${computation_id_unit}'",
                        "inputBoxes": [
                           {
                            "id": "computation_id",
                            "title": "Notwendiger Basis-Indikator",
                            "description": "",
                            "contents": [
                                "computation_id"
                            ]
                            },
                            {
                            "id": "temporal_options",
                            "title": "Notwendiger zeitlicher Bezug",
                            "description": "",
                            "contents": [
                                "number_of_temporal_items",
                                "temporal_type"
                            ]
                            }
                        ]
                    }]
                )
            ]
        ),
        inputs=KommonitorProcess.common_inputs | {
            "computation_id": ProcessInput(
                id= "COMPUTATION_ID",
                title="Auswahl des für die Berechnung erforderlichen Basis-Indikators",
                description="Indikatoren-ID des Basisindikators.",
                schema_=ProcessIOSchema(type_=ProcessIOType.STRING)
            ),
            "number_of_temporal_items": ProcessInput(
                id= "number_of_temporal_items",
                title="Anzahl",
                description= "Anzahl der Zeiteinheiten. Standard ist '1'.",
                schema_=ProcessIOSchema(type_=ProcessIOType.INTEGER, minimum=1, maximum=100000)
            ),
            "temporal_type": ProcessInput(
                id="temporal_type",
                title="Art des zeitlichen Bezugs",
                description="Angabe des Zeitbezug-Typs. Standard ist 'Jahre'.",
                schema_=ProcessIOSchema(
                    type_=ProcessIOType.OBJECT,
                    enum=[
                        {
                        "apiName": "YEARS",
                        "displayName": "Jahr(e)"
                        },
                        {
                            "apiName": "MONTHS",
                            "displayName": "Monat(e)"
                        },
                        {
                            "apiName": "DAYS",
                            "displayName": "Tag(e)"
                        }
                    ],                    
                    default={
                        "apiName": "YEARS",
                        "displayName": "Jahr(e)"
                    }
                )
            )
        }, 
        outputs = KommonitorProcess.common_output
    )

    # run Method has to be implemented for all KomMonitor Skripts
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
        number_of_temporal_items = inputs["number_of_temporal_items"]
        temporal_type = inputs["temporal_type"]

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
            
            # get applicable dates and compute all dates which have to get calculated according to the target_time schema
            computation_indicator_applicable_dates = computation_indicator_metadata.applicable_dates
            target_indicator_applicable_dates = target_indicator_metadata.applicable_dates

            computation_indicator_applicable_spatial_units = []
            for unit in computation_indicator_metadata.applicable_spatial_units:
                computation_indicator_applicable_spatial_units.append(unit.spatial_unit_id)

            all_times = pykmhelper.getAll_target_time(target_time, set(target_indicator_applicable_dates), [set(computation_indicator_applicable_dates)])

            for spatial_unit in target_spatial_units:
                # Init results and job summary for current spatial unit
                result.init_spatial_unit_result(spatial_unit)
                job_summary.init_spatial_unit_summary(spatial_unit)

                # catch missing timestamp error
                missing_dates = [date for date in all_times if not date in computation_indicator_applicable_dates]
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
                
                # find the function, that matches the requested pattern in inputs["temporal_type"]
                if temporal_type == "YEARS":
                    func = pykmhelper.trend_consecutive_n_years
                elif temporal_type == "MONTHS":
                    func = pykmhelper.trend_consecutive_n_months
                elif temporal_type == "DAYS":
                    func = pykmhelper.trend_consecutive_n_days

                # iterate over all features an append the indicator
                indicator_values = []  
                try:
                    for feature in computation_indicator:
                        valueMapping = []
                        for targetTime in all_times:
                            value = func(feature, targetTime, number_of_temporal_items)
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        spatialReferenceKey = feature["ID"]
                        indicator_values.append({"spatialReferenceKey": spatialReferenceKey, "valueMapping": valueMapping})
                except RuntimeError as r:
                    logger.error(r)
                    logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                    job_summary.add_processing_error("INDICATOR", computation_indicator_id, str(r))

                # Job Summary and results
                job_summary.add_number_of_integrated_features(len(indicator_values))
                job_summary.add_integrated_target_dates(all_times)
                job_summary.add_modified_resource(KOMMONITOR_DATA_MANAGEMENT_URL, target_indicator_id, spatial_unit)
                job_summary.complete_spatial_unit_summary()

                result.add_indicator_values(indicator_values)
                result.complete_spatial_unit_result()

                print(result.values)
                 
            # 4.1 Return success and result
            return JobStatus.successful, result, job_summary
        except ApiException as e:

            # 4.2 Catch possible errors cleanly
            return JobStatus.failed, None