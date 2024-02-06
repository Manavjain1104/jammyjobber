import unittest
from unittest.mock import Mock, patch
import numpy as np
from evaluation.evaluation import *


class TestConfusionMatrix(unittest.TestCase):

    def test_confusion_matrix(self):
        # Example data
        true_labels = [1, 2, 3, 4]
        predicted_labels = [1, 2, 4, 4]
        labels = [1, 2, 3, 4]

        # Expected confusion matrix
        expected_output = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1]
        ])

        # Call the function
        result = confusion_matrix(true_labels, predicted_labels, labels)

        # Assert the result is as expected
        np.testing.assert_array_equal(result, expected_output)

    def test_length_mismatch(self):
        # Mismatched lengths should raise an assertion
        true_labels = [1, 2, 3, 4]
        predicted_labels = [1, 2, 3]
        labels = [1, 2, 3, 4]

        # Assert that an assertion is raised due to length mismatch
        with self.assertRaises(AssertionError):
            confusion_matrix(true_labels, predicted_labels, labels)
