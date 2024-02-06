import unittest
from unittest.mock import Mock, patch
import numpy as np
from evaluation.evaluation import *


class TestEvaluationFunctions(unittest.TestCase):

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

    def test_top_n_accuracy(self):
        # Example data
        desired_jobs = ['job1', 'job2', 'job3', 'job4', 'job5']
        recommended_jobs = ['job1', 'job2', 'job4', 'job5', 'job6', 'job7', 'job8']
        n = 4

        # Expected top-4 accuracy
        expected_output = 0.75

        # Call the function
        result = calculate_top_n_accuracy(desired_jobs, recommended_jobs, 4)

        # Assert the result is as expected
        self.assertEqual(result, expected_output)

    def test_hit_rate(self):
        # Example data
        desired_jobs = ['job1', 'job2', 'job3', 'job4', 'job5']
        recommended_jobs = ['job1', 'job2', 'job4', 'job5', 'job6', 'job7', 'job8', 'job10']

        # Expected hit rate
        expected_output = 0.5

        # Call the function
        result = calculate_hit_rate(desired_jobs, recommended_jobs)

        # Assert the result is as expected
        self.assertEqual(result, expected_output)