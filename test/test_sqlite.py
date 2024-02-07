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
            self.connection,
            "Test Job",
            "Test Company",
            "Test Location",
            "Test Description",
            "Test Link",
        )
        self.assertIsNotNone(job_id)
        job = find_job(self.connection, {"id": job_id})
        self.assertEqual(len(job), 1)

    def test_create_same_job_listing(self):
        job_id = create_job_listing(
            self.connection,
            "Test Job",
            "Test Company",
            "Test Location",
            "Test Description",
            "Test Link",
            True,
        )
        self.assertNotEqual(job_id, -1)

        job_id = create_job_listing(
            self.connection,
            "Test Job",
            "Test Company",
            "Test Location",
            "Test Description",
            "Test Link",
            True,
        )
        self.assertEqual(job_id, -1)

    def test_read_empty_job_listing(self):
        jobs = read_job_listings(self.connection)
        self.assertEqual(len(jobs), 0)

    def test_read_job_listing(self):
        populate_dummy_job_listing(self.connection)
        jobs = read_job_listings(self.connection)
        self.assertEqual(len(jobs), 5)

    def test_update_job_listing(self):
        job_id = create_job_listing(
            self.connection,
            "Test Job",
            "Test Company",
            "Test Location",
            "Test Description",
            "Test Link",
        )

        update_job_listing(
            self.connection,
            job_id,
            "Test Job1",
            "Test Company2",
            "Test Location3",
            "Test Description4",
            "Test Link",
        )

        jobs = find_job(self.connection, {"id": job_id})
        self.assertEqual(
            jobs,
            [
                (
                    job_id,
                    "Test Job1",
                    "Test Company2",
                    "Test Location3",
                    "Test Description4",
                    "Test Link",
                )
            ],
        )

    def test_find_job(self):
        create_job_listing(self.connection, "A", "B", "C", "D", "Test Link")
        create_job_listing(self.connection, "A", "E", "F", "J", "Test Link")
        create_job_listing(self.connection, "B", "E", "F", "J", "Test Link")

        jobs = find_job(self.connection, {"title": "A"})
        self.assertEqual(len(jobs), 2)

    def test_delete_job_listing(self):
        a = create_job_listing(self.connection, "A", "B", "C", "D", "Test Link")
        b = create_job_listing(self.connection, "A", "E", "F", "J", "Test Link")

        self.assertEqual(len(read_job_listings(self.connection)), 2)
        delete_job_listing(self.connection, a)
        self.assertEqual(len(read_job_listings(self.connection)), 1)
        delete_job_listing(self.connection, b)
        self.assertEqual(len(read_job_listings(self.connection)), 0)

    def test_delete_empty_job_listing(self):
        self.assertEqual(len(read_job_listings(self.connection)), 0)
        delete_job_listing(self.connection, 1)
        self.assertEqual(len(read_job_listings(self.connection)), 0)

    def test_reset_table(self):
        a = create_job_listing(self.connection, "A", "B", "C", "D", "Test Link")

        jobs = read_job_listings(self.connection)
        self.assertNotEqual(len(jobs), 0)

        reset_table(self.connection)

        jobs = read_job_listings(self.connection)
        self.assertEqual(len(jobs), 0)


if __name__ == "__main__":
    unittest.main()
