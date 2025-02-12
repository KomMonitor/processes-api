import unittest

import pandas as pd

from processor.process.util import dataio


class TestDataio(unittest.TestCase):
    def setUp(self):
        self.base_data = [
            {'DATE_2019-12-31': '36995', 'DATE_2020-12-31': None, 'DATE_2021-12-31': None, 'DATE_2022-12-31': None,
             'DATE_2023-12-31': None, 'ID': 'ID_01', 'NAME': 'Feature 01', 'arisenFrom': None, 'fid': '1',
             'validEndDate': None, 'validStartDate': '2000-01-01'},
            {'DATE_2019-12-31': '17650', 'DATE_2020-12-31': '17446', 'DATE_2021-12-31': '17840',
             'DATE_2022-12-31': '17952', 'DATE_2023-12-31': '18038', 'ID': 'ID_02', 'NAME': 'Feature 02',
             'arisenFrom': None, 'fid': '2', 'validEndDate': None, 'validStartDate': '2000-01-01'},
            {'DATE_2019-12-31': '37373', 'DATE_2020-12-31': '37202', 'DATE_2021-12-31': '37370',
             'DATE_2022-12-31': '37622', 'DATE_2023-12-31': '37656', 'ID': 'ID_03', 'NAME': 'Feature 03',
             'arisenFrom': None, 'fid': '3', 'validEndDate': None, 'validStartDate': '2000-01-01'}
        ]

        self.ref_data = [{
            'DATE_2018-12-31': '75343', 'DATE_2019-12-31': '75437', 'DATE_2020-12-31': '75338',
            'DATE_2021-12-31': '75257', 'DATE_2022-12-31': '76107', 'DATE_2023-12-31': '76808', 'ID': 'ID_01',
            'NAME': 'Feature 01', 'arisenFrom': None, 'fid': '1', 'validEndDate': None,
            'validStartDate': '2000-01-01'},
            {'DATE_2018-12-31': '35808', 'DATE_2019-12-31': '35884', 'DATE_2020-12-31': '35974',
             'DATE_2021-12-31': '36179', 'DATE_2022-12-31': '36495', 'DATE_2023-12-31': '36614',
             'ID': 'ID_02', 'NAME': 'Feature 02', 'arisenFrom': None, 'fid': '2', 'validEndDate': None,
             'validStartDate': '2000-01-01'},
            {'DATE_2018-12-31': '76173', 'DATE_2019-12-31': '76242', 'DATE_2020-12-31': '76032',
             'DATE_2021-12-31': '76125', 'DATE_2022-12-31': '76834', 'DATE_2023-12-31': '78148', 'ID': 'ID_03',
             'NAME': 'Feature 03', 'arisenFrom': None, 'fid': '3', 'validEndDate': None,
             'validStartDate': '2000-01-01'},
            {'DATE_2018-12-31': '78028', 'DATE_2019-12-31': '78076', 'DATE_2020-12-31': '77970',
             'DATE_2021-12-31': '77847', 'DATE_2022-12-31': '78565', 'DATE_2023-12-31': '78484', 'ID': 'ID_04',
             'NAME': 'Feature 04', 'arisenFrom': None, 'fid': '4', 'validEndDate': None,
             'validStartDate': '2000-01-01'},
        ]

        self.target_data = [
            {'DATE_2019-12-31': '36995', 'DATE_2020-12-31': None, 'DATE_2021-12-31': None, 'DATE_2022-12-31': None,
             'ID': 'ID_01', 'NAME': 'Feature 01', 'arisenFrom': None, 'fid': '1',
             'validEndDate': None, 'validStartDate': '2000-01-01'},
            {'DATE_2019-12-31': '17650', 'DATE_2020-12-31': '17446', 'DATE_2021-12-31': '17840',
             'DATE_2022-12-31': '17952', 'ID': 'ID_02', 'NAME': 'Feature 02',
             'arisenFrom': None, 'fid': '2', 'validEndDate': None, 'validStartDate': '2000-01-01'},
            {'DATE_2019-12-31': '37373', 'DATE_2020-12-31': '37202', 'DATE_2021-12-31': '37370',
             'DATE_2022-12-31': '37622', 'ID': 'ID_03', 'NAME': 'Feature 03',
             'arisenFrom': None, 'fid': '3', 'validEndDate': None, 'validStartDate': '2000-01-01'},
        ]

        indicator_df = dataio.indicator_timeseries_to_dataframe(self.base_data)
        ref_indicator_df = dataio.indicator_timeseries_to_dataframe(self.ref_data)
        target_indicator_df = dataio.indicator_timeseries_to_dataframe(self.target_data)

        indicator_df["indicator_id"] = "614618cb-2b7c-479c-8615-6811a1081942"
        ref_indicator_df["indicator_id"] = "1a21b5a6-316b-49d9-8eeb-db420dc435de"
        target_indicator_df["indicator_id"] = "344da619-6c28-4136-895d-ecbc5670f9e7"

        df_list = [indicator_df, ref_indicator_df, target_indicator_df]

        include_timestamps = ["2019-12-31", "2020-12-31"]
        self.input_ids = ["614618cb-2b7c-479c-8615-6811a1081942", "1a21b5a6-316b-49d9-8eeb-db420dc435de"]

        self.dates_df = dataio.get_applicable_dates(df_list)

    def test_get_missing_input_timestamps(self):
        candidates = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=False,
                                                     mode="MISSING")
        self.assertEqual(candidates, [pd.Timestamp("2018-12-31"), pd.Timestamp("2023-12-31")])

        computable = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=True,
                                                     mode="MISSING")
        self.assertEqual(computable, [pd.Timestamp("2023-12-31")])

        missing_input_timestamps = dataio.get_missing_input_timestamps(candidates, self.dates_df, self.input_ids)

        self.assertEqual(missing_input_timestamps[0]["id"], "614618cb-2b7c-479c-8615-6811a1081942")
        self.assertEqual(missing_input_timestamps[0]["missingTimestamps"], [pd.Timestamp("2018-12-31")])

    def test_get_missing_input_timestamps_with_exclude(self):
        exclude = ["2018-12-31"]
        candidates = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=False,
                                                     exclude_dates=exclude,
                                                     mode="MISSING")
        self.assertEqual(candidates, [pd.Timestamp("2023-12-31")])

        computable = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=True,
                                                     exclude_dates=exclude,
                                                     mode="MISSING")
        self.assertEqual(computable, [pd.Timestamp("2023-12-31")])

        missing_input_timestamps = dataio.get_missing_input_timestamps(candidates, self.dates_df, self.input_ids)

        self.assertEqual(len(missing_input_timestamps), 0)

    def test_get_all_input_timestamps(self):
        candidates = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=False,
                                                     mode="ALL")
        self.assertEqual(candidates,
                         [pd.Timestamp("2018-12-31"), pd.Timestamp("2019-12-31"), pd.Timestamp("2020-12-31"),
                          pd.Timestamp("2021-12-31"), pd.Timestamp("2022-12-31"), pd.Timestamp("2023-12-31")])

        computable = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=True,
                                                     mode="ALL")
        self.assertEqual(computable, [pd.Timestamp("2019-12-31"), pd.Timestamp("2020-12-31"),
                                      pd.Timestamp("2021-12-31"), pd.Timestamp("2022-12-31"),
                                      pd.Timestamp("2023-12-31")])

        missing_input_timestamps = dataio.get_missing_input_timestamps(candidates, self.dates_df, self.input_ids)

        self.assertEqual(missing_input_timestamps[0]["id"], "614618cb-2b7c-479c-8615-6811a1081942")
        self.assertEqual(missing_input_timestamps[0]["missingTimestamps"], [pd.Timestamp("2018-12-31")])

    def test_get_all_input_timestamps_with_exclude(self):
        exclude = ["2019-12-31"]
        candidates = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=False,
                                                     exclude_dates=exclude,
                                                     mode="ALL")
        self.assertEqual(candidates,
                         [pd.Timestamp("2018-12-31"), pd.Timestamp("2020-12-31"),
                          pd.Timestamp("2021-12-31"), pd.Timestamp("2022-12-31"), pd.Timestamp("2023-12-31")])

        computable = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=True,
                                                     exclude_dates=exclude,
                                                     mode="ALL")
        self.assertEqual(computable, [pd.Timestamp("2020-12-31"), pd.Timestamp("2021-12-31"),
                                      pd.Timestamp("2022-12-31"), pd.Timestamp("2023-12-31")])

        missing_input_timestamps = dataio.get_missing_input_timestamps(candidates, self.dates_df, self.input_ids)

        self.assertEqual(missing_input_timestamps[0]["id"], "614618cb-2b7c-479c-8615-6811a1081942")
        self.assertEqual(missing_input_timestamps[0]["missingTimestamps"], [pd.Timestamp("2018-12-31")])

    def test_get_selected_input_timestamps(self):
        include = ["2019-12-31"]
        candidates = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=False,
                                                     include_dates=include,
                                                     mode="DATES")
        self.assertEqual(candidates,[pd.Timestamp("2019-12-31")])

        computable = dataio.get_missing_target_dates(self.dates_df,
                                                     target_id="344da619-6c28-4136-895d-ecbc5670f9e7",
                                                     input_ids=self.input_ids,
                                                     drop_input_na=True,
                                                     include_dates=include,
                                                     mode="DATES")
        self.assertEqual(computable, [pd.Timestamp("2019-12-31")])

        missing_input_timestamps = dataio.get_missing_input_timestamps(candidates, self.dates_df, self.input_ids)

        self.assertEqual(len(missing_input_timestamps), 0)
