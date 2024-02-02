import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ADDRESS = os.getenv('LLM_SERVER_ADDRESS')
HEADERS = {'Content-Type': 'application/json'}

# Do locql summary and embedding
DEV_LOCAL = True

if DEV_LOCAL:
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from typing import List

    MAX_LEN = 1000
    MIN_LEN = 30

    summariser = pipeline(
        "summarization", model="Falconsai/text_summarization")
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


def create_summary(text: str) -> str:
    if DEV_LOCAL:
        summariser_output = summariser(
            text, max_length=MAX_LEN, min_length=MIN_LEN, do_sample=False
        )
        summary = summariser_output[0]['summary_text']
        return summary

    json_single_data = json.dumps(text)
    summary_response = requests.post(
        ADDRESS + "get_summary", data=json_single_data, headers=HEADERS)
    if summary_response.status_code == 200:
        summary = summary_response.json()['summary']
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}")

# create one vector embedding given a description in form of a string
# example: create_embedding("some job")


def create_embedding(description):
    if DEV_LOCAL:
        embedding = embedder.encode([description])
        embedding_normalised = embedding / \
            np.linalg.norm(embedding, axis=1, keepdims=True)
        return embedding_normalised[0].tolist()

    json_single_data = json.dumps(description)
    embedding_response = requests.post(
        ADDRESS + "get_embedding", data=json_single_data, headers=HEADERS)
    if embedding_response.status_code == 200:
        embedding = embedding_response.json()['embedding']
        return embedding
    else:
        raise Exception(
            f"Error: {embedding_response.status_code}, {embedding_response.json()}")


# create a list of vector embeddings given a list of descriptions
def bulk_create_embeddings(descriptions):
    if DEV_LOCAL:
        embeddings = embedder.encode(descriptions)
        embeddings_normalised = embeddings / \
            np.linalg.norm(embeddings, axis=1, keepdims=True)
        return list(map(lambda e: e.tolist(), embeddings_normalised))

    json_many_data = json.dumps(descriptions)
    bulk_embedding_response = requests.post(
        ADDRESS + "get_embeddings", data=json_many_data, headers=HEADERS)
    if bulk_embedding_response.status_code == 200:
        bulk_embedding = bulk_embedding_response.json()['embeddings']
        return bulk_embedding
    else:
        raise Exception(
            f"Error: {bulk_embedding_response.status_code}, {bulk_embedding_response.json()}")
