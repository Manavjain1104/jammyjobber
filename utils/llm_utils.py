# pip install -U sentence-transformers requests numpy
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

summariser = pipeline("summarization", model="Falconsai/text_summarization")
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

MAX_LEN = 230
MIN_LEN = 30


def create_summary(text: str) -> str:
    summariser_output = summariser(
        text, max_length=MAX_LEN, min_length=MIN_LEN, do_sample=False
    )
    summary = summariser_output[0]['summary_text']
    return summary

# create one vector embedding given a description in form of a string
# example: create_embedding("some job")


def create_embedding(description):
    embedding = embedder.encode([description])
    embedding_normalised = embedding / \
        np.linalg.norm(embedding, axis=1, keepdims=True)
    return embedding_normalised[0].tolist()


# create a list of vector embeddings given a list of descriptions
def bulk_create_embeddings(descriptions):
    embeddings = embedder.encode(descriptions)
    embeddings_normalised = embeddings / \
        np.linalg.norm(embeddings, axis=1, keepdims=True)
    return list(map(lambda e: e.tolist(), embeddings_normalised))
