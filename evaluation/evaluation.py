import csv
import numpy as np
from numpy.linalg import norm
from context import utils
from utils.llm_utils import create_summary, bulk_create_embeddings, process_data, Model


# ------- HELPER --------
EVAL_COLLECTION_NAME = "Evaluation"
MIN_LEN = 230


def cosine_dist(vec1, vec2):
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    # ------- Evaluation --------


def calculate_recall(desired_jobs, recommended_jobs) -> float:
    """Calculates the hit rate of the recommendations"""
    # initial implementation: we have some way of accessing all desired jobs
    # we compute proportion of top n jobs that are actually desired by user
    hits = 0
    seen = set()

    # we only have a hit if the job is in the top n recommendations and we haven't seen it before
    for desired_job in desired_jobs:
        if desired_job in recommended_jobs and desired_job not in seen:
            hits += 1
            seen.add(desired_job)

    return hits / len(desired_jobs)


def create_embeddings(model, paths_to_csv):
    job_summaries = []
    job_embeddings = []
    hit_job_summaries = []
    hit_job_embeddings = []

    for path_to_csv in paths_to_csv:
        with open(path_to_csv, "r") as csv_file:
            csv_reader = read_csv_columns(
                csv_file,
                ["title", "company", "location", "description", "link", "relevant"],
            )

            for row in csv_reader:
                job_summary = f"The job title is {row['title']}. The company name is {row['company']}, located at {row['location']}. {row['description']}"

                if len(job_summary) > MIN_LEN:
                    job_summary = create_summary(job_summary)

                job_summaries.append(job_summary)

                job_embedding = process_data(job_summary, model)
                job_embeddings.append(job_embedding)

                if row["relevant"] == "TRUE":
                    hit_job_embeddings.append(job_embedding)
                    hit_job_summaries.append(job_summary)

    return job_summaries, job_embeddings, hit_job_embeddings


# PRE: the relevant file is already open
def read_csv_columns(file, columns):
    csv_reader = csv.DictReader(file, delimiter=",")
    headers = next(csv_reader)  # Read the header row to get column names

    # Check if all columns provided are in the headers
    if not all(col in headers.keys() for col in columns):
        raise ValueError(
            "One or more columns provided are not found in the CSV headers."
        )

    return csv_reader


def evaluate(model, query, paths_to_csv):
    """Evaluates the decision tree against the testing data,
    prints the overall accuracy, and the precision, recalls,
    and f1 measures per class

    Args:
        paths_to_csv(lst): path to the csv file
    """
    # In case the information in collection needs to be flushed

    # Process the csv and extract the jobs and qualifications
    job_summaries, job_embeddings, hit_job_embeddings = create_embeddings(
        model, paths_to_csv
    )

    # Process query into embeddings
    request_embedding = process_data(query, model)

    distances = [(e, cosine_dist(request_embedding, e)) for e in job_embeddings]

    n = len(hit_job_embeddings)

    distances_cut_off = sorted(map(lambda x: x[1], distances))[n]

    predictions = [d[0] for d in distances if d[1] < distances_cut_off]

    prediction_hits = 0
    for i in predictions:
        if i in hit_job_embeddings:
            prediction_hits += 1

    print("DEBUG")
    print(len(distances))
    print([d[1] for d in distances])
    print(prediction_hits)
    print(distances_cut_off)
    recall = prediction_hits / n

    print(f"Recall: {recall}")
    return recall


def evaluate_many(paths_to_csv, query_lst, model, noisy=False):
    if len(paths_to_csv) != len(query_lst):
        raise Exception("Number of elements of both should be the same")

    results = []
    for i in range(len(query_lst)):
        print("Evaluating ", paths_to_csv[i])
        results.append(evaluate(model, query_lst[i], paths_to_csv[i]))
    return results


if __name__ == "__main__":
    queryA = """
    I would like to work in accounting. I have a BSc in Maths from Southampton. 
    I want to work for a company with a generous compensation package, 
    and I don't mind working hard and long hours.
    """
    keywordA = "Accountant"

    queryB = """
    I'm looking for my dream job. I care about climate change and I want to work for 
    a company that can help the environment. I'm good with people and a strong leader.
    """
    keywordB = "Sustainability"

    queryC = """
    I am an academic, I have published several high profile papers on molecular biology, 
    genetic engineering, and cellular signalling. I am looking to break into the industry. 
    What jobs are right for me?"""
    keywordC = "Biologist"

    path_to_signalA = "evaluation/accountant.csv"
    path_to_signalB = "evaluation/sustainability.csv"
    path_to_signalC = "evaluation/biologist.csv"
    path_to_noiseA = "evaluation/noise_accountant.csv"
    path_to_noiseB = "evaluation/noise_sustainability.csv"
    path_to_noiseC = "evaluation/noise_biologist.csv"

    models = [Model.EXTRACTOR_DESCRIPTION, Model.NONE, Model.KEYWORD, Model.SUMMARISER]
    for model in models:
        print(f"========== MODEL {model} ==========\n\n")

        print("\n========== METRIC 1 ==========")
        print("3qs with signal".center(30))
        evaluate_many(
            [[path_to_signalA], [path_to_signalB], [path_to_signalC]],
            [queryA, queryB, queryC],
            model,
        )

        print("\n========== METRIC 2 ==========")
        print("3qs with noise".center(30))
        evaluate_many(
            [[path_to_noiseA], [path_to_noiseB], [path_to_noiseC]],
            [queryA, queryB, queryC],
            model,
            True,
        )

        print("\n========== METRIC 3 ==========")
        print("3qs with mixed".center(30))
        evaluate_many(
            [
                [path_to_noiseA, path_to_signalA],
                [path_to_noiseB, path_to_signalB],
                [path_to_noiseC, path_to_signalC],
            ],
            [queryA, queryB, queryC],
            model,
            True,
        )

        print("\n========== METRIC 4 ==========")
        print("extended q with signal".center(30))
        path_to_csv = "evaluation/teacher_ben.csv"

        # query = """I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16.
        # In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare.
        # Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
        # """
        # query = """
        # I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16.
        # In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare.
        # Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
        # I bring to the table experience working with early teenagers, a strong background in math and computer programming, and a six-year focus on STEM subjects.
        # I am personable and adept at handling workplace conflicts.
        # Ideally, I am looking for a school close to public transport, with positive reviews, possibly an Ofsted-rated institution.
        # A reasonably good pay scale would be a welcome addition to the overall package.
        # """
        # wrapper_evaluate_model(model, query, [path_to_csv])
