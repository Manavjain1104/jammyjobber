from context import utils
import utils.semadb_utils as semadb

def test_url_generation():
    assert semadb.collection_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection"
    assert semadb.points_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection/points"
    assert semadb.search_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection/points/search"
    assert semadb.points_url("") == "https://semadb.p.rapidapi.com/collections//points"

test_url_generation()