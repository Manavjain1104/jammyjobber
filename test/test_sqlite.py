from context import utils
from utils.sqlite_utils import *
import unittest
from unittest.mock import Mock, patch


class SqliteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect(":memory:", check_same_thread=False)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        create_table(self.connection)

    def tearDown(self):
        reset_table(self.connection)

    def test_create_job_listing(self):
        job_id = create_job_listing(
            self.connection, "Test Job", "Test Company", "Test Location", "Test Description")
        self.assertIsNotNone(job_id)
        job = find_job(self.connection, {'id': job_id})
        self.assertEqual(len(job), 1)

    def test_create_same_job_listing(self):
        job_id = create_job_listing(
            self.connection, "Test Job", "Test Company", "Test Location", "Test Description", True)
        self.assertNotEqual(job_id, -1)

        job_id = create_job_listing(
            self.connection, "Test Job", "Test Company", "Test Location", "Test Description", True)
        self.assertEqual(job_id, -1)

    def test_read_empty_job_listing(self):
        jobs = read_job_listings(self.connection)
        self.assertEqual(len(jobs), 0)

    def test_read_job_listing(self):
        populate_dummy_job_listing(self.connection)
        jobs = read_job_listings(self.connection)
        self.assertEqual(len(jobs), 5)

    # def test_update_job_listing(self):
    #     ...


if __name__ == '__main__':
    unittest.main()
