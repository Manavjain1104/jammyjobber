import os
import requests
import json

ADDRESS = os.getenv("LLM_SERVER_ADDRESS")
HEADERS = {"Content-Type": "application/json"}


def create_summary(text: str) -> str:
    json_single_data = json.dumps(str)
    summary_response = requests.post(
        ADDRESS + "get_summary", data=json_single_data, headers=HEADERS
    )
    if summary_response.status_code == 200:
        summary = summary_response.json()["summary"]
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}"
        )


# create one vector embedding given a description in form of a string
# example: create_embedding("some job")


def create_embedding(description):
    json_single_data = json.dumps(description)
    embedding_response = requests.post(
        ADDRESS + "get_embedding", data=json_single_data, headers=HEADERS
    )
    if embedding_response.status_code == 200:
        embedding = embedding_response.json()["embedding"]
        return embedding
    else:
        raise Exception(
            f"Error: {embedding_response.status_code}, {embedding_response.json()}"
        )


# create a list of vector embeddings given a list of descriptions
def bulk_create_embeddings(descriptions):
    json_many_data = json.dumps(descriptions)
    bulk_embedding_response = requests.post(
        ADDRESS + "get_embeddings", data=json_many_data, headers=HEADERS
    )
    if bulk_embedding_response.status_code == 200:
        bulk_embedding = bulk_embedding_response.json()["embeddings"]
        return bulk_embedding
    else:
        raise Exception(
            f"Error: {bulk_embedding_response.status_code}, {bulk_embedding_response.json()}"
        )
