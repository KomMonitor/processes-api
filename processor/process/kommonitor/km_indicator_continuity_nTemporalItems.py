from typing import Dict, Optional, Tuple
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

from .. import pykmhelper
from ..pykmhelper import IndicatorCalculationType, IndicatorCollection, IndicatorType

class KmIndicatorContinuityNTemporalItems(KommonitorProcess):
    detailed_process_description = ProcessDescription(
        id="km_indicator_continuity_nTemporalItems",
        version="0.0.1",
        title="Grad der Kontinuität bezogen auf Zeitspanne",
        description= "Berechnet den Grad der Kontinuität über eine vergangene Zeitspanne eines Indikators als Pearson Korrelation bei einer linearen Regression über die betrachtete Zeitspanne.",
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
                        "titleShort": "Kontinuität (mittels Pearson Korrelation)",
                        "apiName": "indicator_continuity",
                        "formula": "$$ r = \frac{\sum_{n=1}^{m}((A_{n} - \bar{A}) \times (I_{n} - \bar{I}))}{\sqrt{\sum_{n=1}^{m} (A_{n} - \bar{A})^2 \times \sum_{n=1}^{m} (I_{n} - \bar{I})^2}} $$",
                        "legend": "<br/>$r$ = Korrelationskoeffizient nach Pearson bei linearer Regression &uuml;ber die betrachtete Zeitspanne <br/>$m$ = Anzahl konsekutiver vergangener Tage/Monate/Jahre <br/>$A_{n}$ = aufeinander folgende Jahre<br/>$\bar{A}$ = arithmetisches Mittel der aufeinander folgenden Jahre<br/>$I_{n}$ = Indikatorenwerte der aufeinander folgenden Jahre<br/>$\bar{I}$ = arithmetisches Mittel der Indikatorenwerte der aufeinander folgenden Jahre",
                        "dynamicLegend": "<br/>$r$ = Korrelationskoeffizient nach Pearson bei linearer Regression &uuml;ber die betrachtete Zeitspanne <br/>$m$ = ${number_of_temporal_items} konsekutiver vergangener ${temporal_type} <br/>$A_{n}$ = aufeinander folgende ${temporal_type}<br/>$\bar{A}$ = arithmetisches Mittel der aufeinander folgenden ${temporal_type}<br/>$I_{n}$ = Indikatorenwerte der aufeinander folgenden ${temporal_type}<br/>$\bar{I}$ = arithmetisches Mittel der Indikatorenwerte der aufeinander folgenden ${temporal_type} <br/> $I$ = Indikator '${compIndicatorSelection.indicatorName} [${compIndicatorSelection.unit}]'",
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
            data_management_client: ApiClient) -> Tuple[JobStatus, KommonitorResult, KommonitorJobSummary]:

        logger.debug("Starting execution...")

         # Load inputs
        inputs = config.inputs
        # Extract all relevant inputs
        target_id = inputs["target_indicator_id"]
        computation_id = inputs["computation_id"]
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

            # create Indicator Objects and IndicatorCollection to store the informations belonging to the Indicator
            ti = IndicatorType(target_id, IndicatorCalculationType.TARGET_INDICATOR)
            
            collection = IndicatorCollection()
            collection.add_indicator(IndicatorType(computation_id, IndicatorCalculationType.COMPUTATION_INDICATOR))
            
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

                # catch missing timestamp error
                if bool_missing_timestamp:
                     collection.check_applicable_target_dates(job_summary)

                # catch missing spatial unit error
                collection.check_applicable_spatial_units(spatial_unit, job_summary)

                # query the correct indicator for all Indicators in Collection
                for indicator in collection.indicators:
                    collection.indicators[indicator].values = indicators_controller.get_indicator_by_spatial_unit_id_and_id_without_geometry(
                        indicator, 
                        spatial_unit)
                    
                collection.fetch_indicator_feature_time_series()

                # get the intersection of all applicable su_features and check for missing spatial unit feature error
                collection.find_intersection_applicable_su_features()
                collection.check_applicable_spatial_unit_features(job_summary)

                logger.debug("Retrieved required indicators successfully")
                
                # find the function, that matches the requested pattern in inputs["temporal_type"]
                if temporal_type == "YEARS":
                    func = pykmhelper.continuity_consecutive_n_years
                elif temporal_type == "MONTHS":
                    func = pykmhelper.continuity_consecutive_n_months
                elif temporal_type == "DAYS":
                    func = pykmhelper.continuity_consecutive_n_days()

                # iterate over all features an append the indicator
                indicator_values = []  
                try:
                    for feature in collection.intersection_su_features:
                        valueMapping = []
                        for targetTime in all_times:
                            value = func(collection.indicators[computation_id].time_series[feature], targetTime, number_of_temporal_items)
                            valueMapping.append({"indicatorValue": value, "timestamp": targetTime})
                        
                        indicator_values.append({"spatialReferenceKey": feature, "valueMapping": valueMapping})
                except RuntimeError as r:
                    logger.error(r)
                    logger.error(f"There occurred an error during the processing of the indicator for spatial unit: {spatial_unit}")
                    job_summary.add_processing_error("INDICATOR", computation_id, str(r))

                # Complete Job Summary and results
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
            logger.error(f"Exception when instantiating DataManagementAPI client: {e}")
            return JobStatus.failed, None