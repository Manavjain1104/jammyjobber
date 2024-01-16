import requests
import os
from dotenv import load_dotenv

base_url = "https://semadb.p.rapidapi.com/collections"

load_dotenv()
KEY = os.getenv('RAPID_API_KEY')
HOST = os.getenv('RAPID_API_HOST')


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
    response = requests.post(base_url, json=payload, headers=headers)
    print(response.json())

create_collection("testcollection", 2)