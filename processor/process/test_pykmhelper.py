import pykmhelper
import unittest
import math
import statistics

class TestPykmhelperZScoreFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = (
            "zScore_byMeanAndStdev",
            "zScore_byPopulationArray",
            "zScore_normalization_wholeValueArray",
        )
        for name in required:
            if not hasattr(pykmhelper, name):
                raise unittest.SkipTest(f"{name} in pykmhelper fehlt")

    def test_zScore_byMeanAndStdev_basic(self):
        value = 10.0
        mean = 5.0
        stdev = 2.0
        res = pykmhelper.zScore_byMeanAndStdev(value, mean, stdev)
        self.assertAlmostEqual(res, (value - mean) / stdev)

    def test_zScore_byPopulationArray_standard_case(self):
        population = [1.0, 2.0, 3.0, 4.0, 5.0]
        # erwartung: z-score von 3.0 ist ~0 (Mittelwert 3)
        z = pykmhelper.zScore_byPopulationArray(3.0, population, computeSampledStandardDeviation=True)
        self.assertAlmostEqual(z, 0.0, places=10)

    # def test_zScore_byPopulationArray_zero_std_raises(self):
    #     # alle Werte identisch -> StdDev == 0 -> Division durch 0 erwartet
    #     population = [5.0, 5.0, 5.0]
    #     with self.assertRaises(Exception):
    #         pykmhelper.zScore_byPopulationArray(5.0, population, computeSampledStandardDeviation=True)

    def test_zScore_normalization_wholeValueArray_standard(self):
        arr = [1.0, 2.0, 3.0]
        out = pykmhelper.zScore_normalization_wholeValueArray(list(arr))
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), len(arr))
        # bei [1,2,3] mit sample-std = 1 sind Z-Scores ~ [-1,0,1]
        self.assertAlmostEqual(out[0], -1.0, places=6)
        self.assertAlmostEqual(out[1],  0.0, places=6)
        self.assertAlmostEqual(out[2],  1.0, places=6)

    def test_zScore_normalization_wholeValueArray_handles_non_numeric(self):
        mixed = [1.0, None, "bad", 3.0]
        # falls helper eine Konvertierungsfunktion anbietet, nutzen wir deren Länge als Erwartung
        if hasattr(pykmhelper, "convertPropertyArrayToNumberArray"):
            expected_len = len(pykmhelper.convertPropertyArrayToNumberArray(mixed))
        else:
            expected_len = len(mixed)
        out = pykmhelper.zScore_normalization_wholeValueArray(list(mixed))
        self.assertEqual(len(out), expected_len)
        # falls mindestens zwei numerische Werte vorhanden sind, sollten diese standardisiert sein
        numeric_only = [v for v in out if v is not None and isinstance(v, (int, float)) and not math.isnan(v)]
        if len(numeric_only) >= 2:
            mean_out = statistics.mean(numeric_only)
            std_out = statistics.pstdev(numeric_only)
            self.assertAlmostEqual(mean_out, 0.0, places=6)
            self.assertGreater(std_out, 0.0)


if __name__ == "__main__":
    unittest.main()