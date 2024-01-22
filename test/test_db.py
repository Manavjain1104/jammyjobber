from context import utils
import utils.semadb_utils as semadb

def test_url_generation():
    assert semadb.collection_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection"

test_url_generation()