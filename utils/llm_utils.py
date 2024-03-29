import os
import requests
import json
from enum import Enum
import numpy as np
from dotenv import load_dotenv

load_dotenv()
ADDRESS = os.getenv("LLM_SERVER_ADDRESS")
TOKEN = os.getenv("INFERENCE_API_TOKEN")
TOKEN = os.getenv("INFERENCE_API_TOKEN")
HEADERS = {"Content-Type": "application/json"}
ANSWERER_MODEL = "deepset/roberta-base-squad2"
FACEBOOk_MODEL = "facebook/bart-large-cnn"
EMBEDDER = "sentence-transformers/all-MiniLM-L12-v2"
SUMMARISER = "Falconsai/text_summarization"


class Model(Enum):
    SUMMARISER = 1
    EXTRACTOR_REQUEST = 2
    EXTRACTOR_DESCRIPTION = 3
    FACEBOOK_SUMMARISER = 4
    SUMMARY_ONLY = 5
    NONE = 6


def process_data(text, model):
    if model == Model.SUMMARISER:
        embedding = create_embedding(create_summary(text))
        return embedding
    elif model == Model.EXTRACTOR_DESCRIPTION:
        # 768 vector model
        return create_embedding(get_job_details(text)) + create_embedding(
            get_skills_required(text)
        )
    elif model == Model.EXTRACTOR_REQUEST:
        return create_embedding(get_suggested_job(text)) + create_embedding(
            get_candidate_skills(text)
        )
    # elif model == Model.FACEBOOK_SUMMARISER:
    #     return create_embedding(create_summary_facebook_model(text))
    elif model == Model.NONE:
        return create_embedding(text)
    elif model == Model.SUMMARY_ONLY:
        return create_summary(text)
    else:
        raise Exception("Unknown model")


def create_summary(text: str) -> str:
    json_single_data = json.dumps(text)
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


# def create_summary_facebook_model(text):
#     client = InferenceClient(token=TOKEN,
#                              model=FACEBOOk_MODEL)
#     answer = client.summarization(text)
#     return answer

# create one vector embedding given a description in form of a string
# example: create_embedding("some job")


def get_skills_required(description):
    json_single_data = json.dumps(description)
    summary_response = requests.post(
        ADDRESS + "get_skills_required", data=json_single_data, headers=HEADERS
    )
    if summary_response.status_code == 200:
        summary = summary_response.json()["answer"]
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}"
        )


def get_job_details(description):
    json_single_data = json.dumps(description)
    summary_response = requests.post(
        ADDRESS + "get_job_details", data=json_single_data, headers=HEADERS
    )
    if summary_response.status_code == 200:
        summary = summary_response.json()["answer"]
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}"
        )


def get_candidate_skills(request):
    json_single_data = json.dumps(request)
    summary_response = requests.post(
        ADDRESS + "get_candidate_skills", data=json_single_data, headers=HEADERS
    )
    if summary_response.status_code == 200:
        summary = summary_response.json()["answer"]
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}"
        )


def get_suggested_job(request):
    json_single_data = json.dumps(request)
    summary_response = requests.post(
        ADDRESS + "get_suggested_job", data=json_single_data, headers=HEADERS
    )
    if summary_response.status_code == 200:
        summary = summary_response.json()["answer"]
        return summary
    else:
        raise Exception(
            f"Error: {summary_response.status_code}, {summary_response.json()}"
        )


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
