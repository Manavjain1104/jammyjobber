import requests
import os
from dotenv import load_dotenv

base_url = "https://semadb.p.rapidapi.com/collections"

# Get variables from the environment
load_dotenv()
KEY = os.getenv('RAPID_API_KEY')
HOST = os.getenv('RAPID_API_HOST')

# Collection name
COLLECTION_NAME = "JobListings"


# Url used to access a collection
def collection_url(collection):
    return base_url + "/" + collection


# Url used to add points to a collection
def points_url(collection):
    return collection_url(collection) + "/points"


# Url used to search for points
def search_url(collection):
    return points_url(collection) + "/search"


# Create a new collection of points
def create_collection(id, vectorSize, distanceMetric="cosine"):
    payload = {
        "id": id,
        "vectorSize": vectorSize,
        "distanceMetric": distanceMetric
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    response = requests.post(base_url, json=payload, headers=headers)
    return response.json()


# Given vector representation and SQLite id, return json representation
# of a point
def new_point(vector, externalId):
    return {"vector": vector, "metadata": {"externalId": externalId}}


# Given vector representation of a point and an id used in SQLite,
# add the point to the specified collection
# example: add_points("testcollection", [new_point([4.2, 2.4], 23)])
def add_points(collection, points):
    payload = {"points": points}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    response = requests.post(points_url(collection),
                             json=payload, headers=headers)
    return response


# Add points to a collection given a list of vector embeddings and their external ids
def bulk_add_points(collection, vectors, ids):
    points = []
    for point in zip(vectors, ids):
        points.append(new_point(point[0], point[1]))
    return add_points(collection, points)


# Given a collection name, retrieve basic information about the collection
def get_collection(collection):
    headers = {
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    response = requests.get(collection_url(collection), headers=headers)
    return response.json()


# Given a vector representation of a point, search for limit nearest points
# in the database. Returns a list of job ids, used in SQLite
def search_points(collection, vector, limit=10):
    payload = {
        "vector": vector,
        "limit": limit
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    response = requests.post(search_url(collection),
                             json=payload, headers=headers)

    point_ids = []
    for point in response.json()['points']:
        point_ids.append(point['metadata']['externalId'])

    return point_ids
