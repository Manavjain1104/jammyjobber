from ../semadb_utils import *

def test_url_generation():
    assert collection_url("test_collection") == "https://semadb.p.rapidapi.com/collections/test_collection"

test_url_generation()