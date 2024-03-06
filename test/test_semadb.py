from unittest import mock

from context import utils
import utils.semadb_utils as semadb
import unittest
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none


test_collection = "test_collection"


class SemaDBTestCase(unittest.TestCase):
    def test_url_generation(self):
        assert (
            semadb.collection_url(test_collection)
            == "https://semadb.p.rapidapi.com/collections/test_collection"
        )
        assert (
            semadb.points_url(test_collection)
            == "https://semadb.p.rapidapi.com/collections/test_collection/points"
        )
        assert (
            semadb.search_url(test_collection)
            == "https://semadb.p.rapidapi.com/collections/test_collection/points/search"
        )
        assert (
            semadb.points_url("") == "https://semadb.p.rapidapi.com/collections//points"
        )

    def test_points_generation(self):
        vector = [1.0, 1.0]
        id = 1
        assert semadb.new_point(vector, id) == {
            "id": id,
            "vector": vector
        }
        with self.assertRaises(Exception):
            semadb.new_point()

    @patch("utils.semadb_utils.requests.get")
    def test_get_collection_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = semadb.get_collection(test_collection)
        assert_is_not_none(response)

    @patch("utils.semadb_utils.requests.post")
    def test_add_points_ok(self, mock_post):
        mock_post.return_value.ok = True
        response = semadb.add_points(test_collection, [semadb.new_point([1, 1], 1)])
        assert_is_not_none(response)

    def test_bulk_add_calls_add_points(self):
        mock_function_module = "utils.semadb_utils"
        mock_function = f"{mock_function_module}.add_points"

        new_points_vectors = [[1, 1], [2, 2]]
        new_points_ids = [1, 2]

        response = "ok response; points added"
        with mock.patch(mock_function, return_value=response):
            assert (
                semadb.bulk_add_points(
                    test_collection, new_points_vectors, new_points_ids
                )
                == response
            )

    @patch("utils.semadb_utils.requests.post")
    def test_search_points(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {
            "points": [
                {"id": "point_id", "distance": 1, "metadata": {"externalId": 1284}}
            ]
        }
        response = semadb.search_points(test_collection, [1, 1], 1)
        assert response == [1284]

    @patch("utils.semadb_utils.requests.get")
    def test_get_collection_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = semadb.get_collection(test_collection)
        assert_is_not_none(response)

    @patch("utils.semadb_utils.requests.post")
    def test_add_points_ok(self, mock_post):
        mock_post.return_value.ok = True
        response = semadb.add_points(test_collection, [semadb.new_point([1, 1], 1)])
        assert_is_not_none(response)

    def test_bulk_add_calls_add_points(self):
        mock_function_module = "utils.semadb_utils"
        mock_function = f"{mock_function_module}.add_points"

        new_points_vectors = [[1, 1], [2, 2]]
        new_points_ids = [1, 2]

        response = "ok response; points added"
        with mock.patch(mock_function, return_value=response):
            assert (
                semadb.bulk_add_points(
                    test_collection, new_points_vectors, new_points_ids
                )
                == response
            )

    @patch("utils.semadb_utils.requests.post")
    def test_search_points(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {
            "points": [
                {"id": "point_id", "distance": 1, "metadata": {"externalId": 1284}}
            ]
        }
        response = semadb.search_points(test_collection, [1, 1], 1)
        assert response == [1284]

    @patch("utils.semadb_utils.requests.get")
    def test_get_collection_ok(self, mock_get):
        mock_get.return_value.ok = True
        response = semadb.get_collection(test_collection)
        assert_is_not_none(response)

    @patch("utils.semadb_utils.requests.post")
    def test_add_points_ok(self, mock_post):
        mock_post.return_value.ok = True
        response = semadb.add_points(test_collection, [semadb.new_point([1, 1], 1)])
        assert_is_not_none(response)

    def test_bulk_add_calls_add_points(self):
        mock_function_module = "utils.semadb_utils"
        mock_function = f"{mock_function_module}.add_points"

        new_points_vectors = [[1, 1], [2, 2]]
        new_points_ids = [1, 2]

        response = "ok response; points added"
        with mock.patch(mock_function, return_value=response):
            assert (
                semadb.bulk_add_points(
                    test_collection, new_points_vectors, new_points_ids
                )
                == response
            )

    @patch("utils.semadb_utils.requests.post")
    def test_search_points(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {
            "points": [
                {"id": 1284, "distance": 1}
            ]
        }
        response = semadb.search_points(test_collection, [1, 1], 1)
        assert response == ([1284], [1])


if __name__ == "__main__":
    unittest.main()
