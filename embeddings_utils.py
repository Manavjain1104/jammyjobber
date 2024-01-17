# pip install -U sentence-transformers requests numpy
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# create one vector embedding given a description in form of a string
# example: create_embedding("some job")
def create_embedding(description):
    embedding = model.encode([description])
    embedding_normalised = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
    return embedding_normalised[0].tolist()


# create a list of vector embeddings given a list of descriptions
def bulk_create_embeddings(descriptions):
    embeddings = model.encode(descriptions)
    embeddings_normalised = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return list(map(lambda e: e.tolist(), embeddings_normalised))
