import unittest
from evaluation.evaluation import *


conf_matrix = np.array([
     [18, 1, 0, 0, 1, 0],
     [2, 15, 3, 0, 0, 0],
     [0, 2, 20, 1, 1, 1],
     [0, 0, 2, 22, 1, 0],
     [1, 0, 0, 2, 17, 0],
     [0, 0, 0, 1, 0, 19]
])


class TestEvaluationFunctions(unittest.TestCase):

    def test_confusion_matrix(self):
        true_labels = [1, 2, 3, 4]
        predicted_labels = [1, 2, 4, 4]
        labels = [1, 2, 3, 4]
        expected_output = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1]
        ])

        result = confusion_matrix(true_labels, predicted_labels, labels)
        np.testing.assert_array_equal(result, expected_output)

    def test_length_mismatch(self):
        true_labels = [1, 2, 3, 4]
        predicted_labels = [1, 2, 3]
        labels = [1, 2, 3, 4]

        with self.assertRaises(AssertionError):
            confusion_matrix(true_labels, predicted_labels, labels)

    def test_top_n_accuracy(self):
        # Example data
        desired_jobs = ['job1', 'job2', 'job3', 'job4', 'job5']
        recommended_jobs = ['job1', 'job2', 'job4', 'job5', 'job6', 'job7', 'job8']
        n = 4

        expected_output = 0.75
        result = calculate_top_n_accuracy(desired_jobs, recommended_jobs, 4)
        self.assertEqual(result, expected_output)

    def test_hit_rate(self):
        desired_jobs = ['job1', 'job2', 'job3', 'job4', 'job5']
        recommended_jobs = ['job1', 'job2', 'job4', 'job5', 'job6', 'job7', 'job8', 'job10']

        expected_output = 0.5
        result = calculate_hit_rate(desired_jobs, recommended_jobs)
        self.assertEqual(result, expected_output)

    def test_accuracy(self):
        expected_output = 0.8538
        result = calculate_accuracy(conf_matrix)
        self.assertEqual(round(result, 4), expected_output)

    def test_precisions(self):
        expected_output = [0.8571, 0.8333, 0.8, 0.8462, 0.85, 0.95]
        result = calculate_precisions(conf_matrix)
        print(result)
        for i in range(len(result)):
            self.assertEqual(round(result[i], 4), expected_output[i])

    def test_recalls(self):
        expected_output = [0.9, 0.75, 0.8, 0.88, 0.85, 0.95]
        result = calculate_recalls(conf_matrix)
        for i in range(len(result)):
            self.assertEqual(round(result[i], 4), expected_output[i])

    def test_f1_scores(self):
        expected_output = [0.878, 0.7895, 0.8, 0.8627, 0.85, 0.95]
        result = calculate_f1_measures(conf_matrix)
        for i in range(len(result)):
            self.assertEqual(round(result[i], 4), expected_output[i])