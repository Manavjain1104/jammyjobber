from context import utils
import utils.semadb_utils as semadb
import unittest
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none

class SemaDBTestCase(unittest.TestCase):
    def test_url_generation(self):
        assert semadb.collection_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection"
        assert semadb.points_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection/points"
        assert semadb.search_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection/points/search"
        assert semadb.points_url("") == "https://semadb.p.rapidapi.com/collections//points"

    def test_points_generation(self):
        vector = [1.0, 1.0]
        externalId = 1
        assert semadb.new_point(vector, externalId) == {"vector":  vector, "metadata": {"externalId": externalId}}
        with self.assertRaises(Exception):
            semadb.new_point()

    @patch('utils.semadb_utils.requests.get')
    def test_get_collection_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = semadb.get_collection("test_collection")
        assert_is_not_none(response)

if __name__ == '__main__':
    unittest.main()