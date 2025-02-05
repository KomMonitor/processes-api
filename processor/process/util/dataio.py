import pandas as pd
import itertools

from openapi_client import IndicatorOverviewType


def indicator_timeseries_to_dataframe(timeseries: list, indicator_id: str = None, spatial_unit_id:str = None, date_col: str = "date", value_col: str = "value") -> pd.DataFrame:
    """Creates a pd.DataFrame from indicator timeseries values for a single spatial unit

    Args:
        indicator_id: Identifier of the indicator, which will be added as column
        spatial_unit_id: Identifier of the spatial unit, which will be added as column
        timeseries: Timeseries data for a single spatial unit
        date_col: Name of the date column. Default: "date"
        value_col: Name of the column that contains timeseries values. Default: "value"

    Returns:
        A pd.DataFrame that contains timeseries values for all features of a single spatial unit

    """
    df = pd.DataFrame(timeseries)
    df = df.melt(id_vars=["ID", "NAME", "arisenFrom", "fid", "validStartDate", "validEndDate"],
                                     var_name=date_col, value_name=value_col)
    df = df[["ID", date_col, value_col]]
    if indicator_id:
        df["indicator_id"] = indicator_id
    if spatial_unit_id:
        df["spatial_unit_id"] = spatial_unit_id
    df["date"] = pd.to_datetime(df["date"], format="DATE_%Y-%m-%d")
    return df


def dataframe_to_indicator_timeseries(df: pd.DataFrame, id_col: str = "ID", date_col: str = "date", value_col: str = "result") -> list:
    """Creates indicator timeseries results as dict from a pd.DataFrame

    Args:
        df: DataFrame that contains indicator timeseries values for several features of a single spatial unit
        id_col: Name of the ID column. Default: "ID"
        date_col:: Name of the date column: Default: "date"
        value_col: Name of the column that contains the timeseries values. Default: "result"

    Returns:
        Timeseries results for a single spatial unit as list of dicts such as:

        {
            "applicableSpatialUnit": "dictricts",
            "indicatorValues": [
                {
                    "spatialReferenceKey": "1",
                    "valueMapping": [
                        {
                            "indicatorValue": 0,
                            "timestamp": "2025-01-15"
                        },
                        {
                            "indicatorValue": 1,
                            "timestamp": "2024-01-15"
                        }
                    ]
                },
                {
                    "spatialReferenceKey": "2",
                    "valueMapping": [
                        {
                            "indicatorValue": 10,
                            "timestamp": "2025-01-15"
                        },
                        {
                            "indicatorValue": 6,
                            "timestamp": "2024-01-15"
                        }
                    ]
                },
                ... // for all 50 disctricts
            ]
        }

    """
    grouped_df = df.groupby(id_col)

    results = []

    for feature_id, group in grouped_df:
        feature_result = {
            "spatialReferenceKey": feature_id,
            "valueMapping": []
        }
        for index, row in group.iterrows():
            timestep_result = {
                "indicatorValue": row[value_col],
                "timestamp": row[date_col].strftime("%Y-%m-%d")
            }
            feature_result["valueMapping"].append(timestep_result)
        results.append(feature_result)
    return results


def get_unique_dates(dates: list) -> set:
    return set(itertools.chain.from_iterable(dates))


def get_applicable_dates_from_metadata_as_dataframe(metadata_list: list[IndicatorOverviewType]) -> pd.DataFrame:
    date_list = []
    date_dict_list = []
    for m in metadata_list:
        date_list.append(m.applicable_dates)
        date_dict_list.append({"id": m.indicator_id, m.indicator_id: m.applicable_dates})
    unique_dates = get_unique_dates(date_list)
    df = pd.DataFrame(unique_dates, columns=["date"]).sort_values(by="date")
    for d in date_dict_list:
        df = df.merge(pd.DataFrame(d)[[d["id"]]], left_on="date", right_on=d["id"], how="outer")
    return df


def get_applicable_dates(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    dates_df = pd.DataFrame(pd.concat(df_list)["date"].unique(), columns=["date"]).sort_values(by="date")
    for df in df_list:
        i_df = pd.DataFrame({df["indicator_id"][0]: df["date"].unique()})
        i_id = df["indicator_id"][0]
        dates_df = dates_df.merge(i_df, left_on="date", right_on=i_id, how="outer")
    return dates_df


def get_missing_target_dates(df: pd.DataFrame, target_id: str, input_ids: list[str], drop_input_na: bool, mode: str = "MISSING", include_dates: list =[], exclude_dates: list = []):
    include_dates = [pd.Timestamp(d) for d in include_dates]
    exclude_dates = [pd.Timestamp(d) for d in exclude_dates]

    if drop_input_na:
        df = df.dropna(subset=input_ids)
    if mode == "MISSING":
        df = df[["date"]][df[target_id].isnull()]
        return list(df["date"][~df["date"].isin(exclude_dates)])
    elif mode == "ALL":
        return list(df["date"][~df["date"].isin(exclude_dates)])
    elif mode == "DATES":
        if drop_input_na:
            return list(df["date"][df["date"].isin(include_dates)])
        else:
            return include_dates


def get_missing_input_timestamps(target_dates: list, df: pd.DataFrame, input_ids: list) -> list:
    target_dates_series = pd.Series(target_dates)
    missing_timestamp_list = []
    for id in input_ids:
        missing_timestamps = list(target_dates_series[~target_dates_series.isin(df[id])])
        if(len(missing_timestamps) > 0):
            missing_timestamp_list.append({"id": id, "missingTimestamps": missing_timestamps})
    return missing_timestamp_list
