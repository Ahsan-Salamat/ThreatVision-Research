import unittest

import numpy as np

from research.preprocessing import tensor
from research.train import _preprocess_tf_bytes


class TrainInputTests(unittest.TestCase):
    def test_tf_numpy_function_bytes_match_research_preprocessing(self):
        raw = b"MZ synthetic training smoke fixture"
        actual = _preprocess_tf_bytes(raw)
        expected = tensor(raw)
        self.assertEqual(actual.shape, (1, 224, 224, 1))
        self.assertEqual(actual.dtype, np.float32)
        np.testing.assert_array_equal(actual, expected)


if __name__ == "__main__":
    unittest.main()
