import requests
import os
from dotenv import load_dotenv

base_url = "https://semadb.p.rapidapi.com/collections"
points_url = "https://semadb.p.rapidapi.com/collections/mycollection/points"

load_dotenv()
KEY = os.getenv('RAPID_API_KEY')
HOST = os.getenv('RAPID_API_HOST')


def collection_url(collection):
    return base_url + "/" + collection


# url to work with separate points from a collection
def points_url(collection):
    return collection_url(collection) + "/points"

def search_url(collection):
    return points_url(collection) + "/search"


# function to create a new collection of points
def create_collection(id, vectorSize, distanceMetric="euclidean"):
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
    requests.post(base_url, json=payload, headers=headers)


def new_point(vector, externalId):
    return {"vector": vector, "metadata": {"externalId": externalId}}

# example: add_points("testcollection", [new_point([4.2, 2.4], 23)])
def add_points(collection, points):
    payload = {"points": points}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    requests.post(points_url(collection), json=payload, headers=headers)


def get_collection(collection):
    headers = {
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }
    requests.get(collection_url(collection), headers=headers)


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
    response = requests.post(search_url(collection), json=payload, headers=headers)

    point_ids = []
    for point in response.json()['points']:
        point_ids.append(point['metadata']['externalId'])

    return point_ids
