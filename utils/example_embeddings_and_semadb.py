from semadb_utils import *
from llm_utils import *

# create_collection("testJobs", 384, "cosine")
jobs = [
    "This is a Software Engineering job.",
    "You will be a receptionist at our clinic.",
    "We are looking for a python developer. We can offer a competetive salary",
    "Charity worker needed.",
    "Dog sitter job in Manchester",
]
# embedding_1 = create_embedding(jobs[0])
# embedding_2 = create_embedding(jobs[1])
# add_points("testJobs", [new_point(embedding_1, 0),
#                          new_point(embedding_2, 1)])

# bulk_add_points("testJobs", create_bulk_embeddings(jobs2), [3, 4])
# get_collection("testJobs")


# job = "Only London"
# print(job)
# #
# request_embedding = create_embedding(job)
# print(len(request_embedding))
# closest = search_points("testJobs", request_embedding, 1)
# print(jobs[closest[0]])


# print(create_collection(COLLECTION_NAME, 384))


print(get_collection(COLLECTION_NAME))
