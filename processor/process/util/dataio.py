import pandas as pd

def indicator_timeseries_to_dataframe(timeseries: list, date_col: str = "date", value_col: str = "value") -> pd.DataFrame:
    """Creates a pd.DataFrame from indicator timeseries values for a single spatial unit

    Args:
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
    df["date"] = pd.to_datetime(df["date"], format="DATE_%Y-%m-%d")
    return df


def dataframe_to_indicator_timeseries(df: pd.DataFrame, id_col: str = "ID", date_col: str = "date", value_col: str = "result") -> dict:
    """Creates indicator timeseries results as dict from a pd.DataFrame

    Args:
        df: DataFrame that contains indicator timeseries values for several features of a single spatial unit
        id_col: Name of the ID column. Default: "ID"
        date_col:: Name of the date column: Default: "date"
        value_col: Name of the column that contains the timeseries values. Default: "result"

    Returns:
        Timeseries results for a single spatial unit as dict such as:

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

    results = {
        "applicableSpatialUnit": "stadtteile",
        "indicatorValues": []
    }

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
        results["indicatorValues"].append(feature_result)
    return results
