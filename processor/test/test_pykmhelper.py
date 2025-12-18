import processor.process.pykmhelper as pykmhelper
import unittest
import math
import statistics
import numpy as np

class TestPykmhelperZScoreFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = (
            "zScore_byMeanAndStdev",
            "zScore_byPopulationArray",
            "zScore_normalization_wholeValueArray",
            "zScore_normalization_wholeValueArray_inverted",
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
        
    def test_zScore_normalization_wholeValueArray_standard(self):
        arr = [1.0, 2.0, 3.0]
        out = pykmhelper.zScore_normalization_wholeValueArray(list(arr))
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), len(arr))
        # bei [1,2,3] mit sample-std = 1 sind Z-Scores ~ [-1.224744871, 0, 1.224744871] je nach Implementierung
        self.assertAlmostEqual(out[0], -1.224744871, places=6)
        self.assertAlmostEqual(out[1],  0.0, places=6)
        self.assertAlmostEqual(out[2],  1.224744871, places=6)

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

    def test_zScore_normalization_wholeValueArray_inverted_standard(self):
        arr = [1.0, 2.0, 3.0]
        out = pykmhelper.zScore_normalization_wholeValueArray(list(arr))
        out_inv = pykmhelper.zScore_normalization_wholeValueArray_inverted(list(arr))
        self.assertIsInstance(out_inv, list)
        self.assertEqual(len(out_inv), len(arr))

        numeric_inv = [v for v in out_inv if v is not None and isinstance(v, (int, float)) and not math.isnan(v)]
        if len(numeric_inv) >= 2:
            mean_inv = statistics.mean(numeric_inv)
            std_inv = statistics.pstdev(numeric_inv)
            self.assertAlmostEqual(mean_inv, 1.0, places=6)
            self.assertGreater(std_inv, 0.0)

    def test_zScore_normalization_wholeValueArray_inverted_handles_non_numeric(self):
        mixed = [1.0, None, "bad", 3.0]
        if hasattr(pykmhelper, "convertPropertyArrayToNumberArray"):
            expected_len = len(pykmhelper.convertPropertyArrayToNumberArray(mixed))
        else:
            expected_len = len(mixed)
        out_inv = pykmhelper.zScore_normalization_wholeValueArray_inverted(list(mixed))
        self.assertEqual(len(out_inv), expected_len)
        numeric_only = [v for v in out_inv if v is not None and isinstance(v, (int, float)) and not math.isnan(v)]
        if len(numeric_only) >= 2:
            mean_out = statistics.mean(numeric_only)
            std_out = statistics.pstdev(numeric_only)
            self.assertAlmostEqual(mean_out, 1.0, places=6)
            self.assertGreater(std_out, 0.0)

    def test_geomean_standard(self):
        """Test geomean with standard positive values."""
        arr = [1.0, 2.0, 4.0, 8.0]
        result = pykmhelper.geomean(arr)
        self.assertIsInstance(result, (int, float))
        # geomean([1,2,4,8]) = (1*2*4*8)^(1/4) = 64^0.25 = 2.828...
        expected = (1.0 * 2.0 * 4.0 * 8.0) ** (1.0 / 4.0)
        self.assertAlmostEqual(result, expected, places=6)

    def test_geomean_negative_values(self):
        """Test geomean with negative values."""
        arr = [1.0, -2.0, 4.0, -8.0]
        with self.assertRaises(RuntimeError):
            pykmhelper.geomean(arr)
            
    def test_geomean_identical_values(self):
        """Test geomean with identical values."""
        arr = [5.0, 5.0, 5.0]
        result = pykmhelper.geomean(arr)
        # geomean von identischen Werten sollte dieser Wert selbst sein
        self.assertAlmostEqual(result, 5.0, places=6)

    def test_geomean_single_value(self):
        """Test geomean with a single value."""
        arr = [7.0]
        result = pykmhelper.geomean(arr)
        self.assertAlmostEqual(result, 7.0, places=6)

    def test_geomean_handles_non_numeric(self):
        """Test geomean with mixed/non-numeric values."""
        mixed = [1.0, None, "bad", 4.0]
        if hasattr(pykmhelper, "convertPropertyArrayToNumberArray"):
            numeric = pykmhelper.convertPropertyArrayToNumberArray(mixed)
            result = pykmhelper.geomean(mixed)
            # geomean sollte nur auf numerische Werte angewendet werden
            expected = pykmhelper.geomean(numeric)
            self.assertAlmostEqual(result, expected, places=6)
        else:
            # Falls keine Konvertierungsfunktion existiert, erwarten wir dass geomean selbst damit umgeht
            try:
                result = pykmhelper.geomean(mixed)
                self.assertIsInstance(result, (int, float))
            except (TypeError, ValueError):
                # Akzeptabel wenn geomean keine non-numerischen Werte verarbeitet
                pass


if __name__ == "__main__":
    unittest.main()