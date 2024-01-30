import json
import requests
from context import utils
from utils.llm_utils import create_embedding
from csv import reader
import numpy as np
from numpy.linalg import norm
from numpy import dot


# ------- HELPER --------
SUMMARISER_URL = 'http://127.0.0.1:5000/summariser'
EVAL_COLLECTION_NAME = "Evaluation"
MIN_LEN = 230


def cosine_dist(vec1, vec2):
    return np.dot(vec1, vec2)/(norm(vec1) * norm(vec2))

# ------- Evaluation --------


def confusion_matrix(true_labels, predicted_labels, labels) -> np.ndarray:
    """Creates a confusion matrix based on the true and predicted labels"""
    assert len(true_labels) == len(
        predicted_labels), "The number of true labels and predicted labels must be the same"

    # create a dictionary mapping labels to indices
    label_to_index = {label: i for i, label in enumerate(labels)}

    # initialise the confusion matrix to be np array of zeros
    conf_matrix = np.zeros((len(labels), len(labels)), dtype=np)

    # populate the confusion matrix
    for true_label, predicted_label in zip(true_labels, predicted_labels):
        true_index = label_to_index[true_label]
        predicted_index = label_to_index[predicted_label]
        conf_matrix[true_index, predicted_index] += 1

    return conf_matrix


def calculate_top_n_accuracy(desired_job, recommended_jobs, n):
    """Calculates the top n accuracy of the recommendations"""
    pass


def calculate_hit_rate(desired_jobs, recommended_jobs) -> float:
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

    return hits / len(recommended_jobs)


def calculate_accuracy(conf_matrix) -> float:
    """Calculates the accuracy from the confusion matrix"""
    true_positives = np.trace(conf_matrix)
    total_predictions = np.sum(conf_matrix)
    accuracy = true_positives / total_predictions
    return accuracy


def calculate_precisions(conf_matrix):
    precisions = []
    for i in range(len(conf_matrix)):
        true_pos = conf_matrix[i, i]
        false_pos = np.sum(conf_matrix[:, i]) - true_pos
        precision = true_pos / (true_pos + false_pos)
        precisions.append(precision)
    return precisions


def calculate_recalls(conf_matrix):
    recalls = []
    for i in range(len(conf_matrix)):
        true_pos = conf_matrix[i, i]
        false_neg = np.sum(conf_matrix[i, :]) - true_pos
        recall = true_pos / (true_pos + false_neg)
        recalls.append(recall)
    return recalls


def calculate_f1_measures(conf_matrix):
    precisions = calculate_precisions(conf_matrix)
    recalls = calculate_recalls(conf_matrix)
    f1_measures = []
    for precision, recall in zip(precisions, recalls):
        f1 = 2 * (precision * recall) / (precision + recall)
        f1_measures.append(f1)
    return f1_measures

# ------- Matrix ---------


def find_dynamic_cutoff(distances, sensitivity=2.0):
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)

    # Detect outliers using the Z-score
    z_scores = [(dist - mean_distance) / std_distance for dist in distances]

    # Identify the index where a sudden change occurs (assuming a single cluster of distances)
    change_index = np.argmax(np.abs(np.diff(z_scores)) > sensitivity)

    # Use the detected change point as the dynamic threshold
    dynamic_threshold = distances[change_index +
                                  1] if change_index < len(distances) - 1 else distances[-1]

    labels = [str(dist <= dynamic_threshold) for dist in distances]
    return labels


def add_points_to_datbase(path_to_csv):
    with open(path_to_csv, 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        csv_header = next(csv_reader)

        if csv_header != ["title", "company", "location", "description", "link", 'want to get', 'ranking']:
            raise Exception(
                "csv file should contain title, company, location, description, link (order matters)")

        true_labels = []
        job_embeddings = []
        job_summaries = []

        # Populate the semaDB (we do not need to create the sqlite)
        for row in csv_reader:
            true_labels.append(row[5])  # true or false

            # Assuming that header start as {title, company, location, description}
            job_summary = f"The job title is {row[0]}. The company name is {row[1]}, located at {row[2]}. {row[3]}"

            if len(job_summary) > MIN_LEN:
                data = {'text': job_summary}
                json_data = json.dumps(data)
                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    SUMMARISER_URL, data=json_data, headers=headers)

                if response.status_code == 200:
                    job_summary = response.json()['summary']
                    job_embedding = response.json()['embedding']
                    job_embeddings.append(job_embedding)
                else:
                    raise Exception(
                        f"Error: {response.status_code}, {response.json()}")
            job_summaries.append(job_summary)

    # bulk_add_points(EVAL_COLLECTION_NAME, job_embeddings,range(len(true_labels)))

    return (true_labels, job_summaries, job_embeddings)


def evaluate(path_to_csv, query, reset=False):
    """Evaluates the decision tree against the testing data,
    prints the overall accuracy, and the percision, recalls,
    and f1 measures per class

    Args:
        path_to_csv(str): path to the csv file
    """

    # In case the information in collection needs to be flushed

    # Process the csv and extract the jobs and qualifications
    true_labels, job_summaries, job_embeddings = add_points_to_datbase(
        path_to_csv)

    # Process query in our semaDB to see the returns
    request_embedding = create_embedding(query)

    distances = [cosine_dist(request_embedding, entry_embedding)
                 for entry_embedding in job_embeddings]  # in order

    predicted_labels = find_dynamic_cutoff(distances)
    labels = ["True", "False"]

    # Create a confusion matrix based on the labels
    conf_matrix = confusion_matrix(
        true_labels, predicted_labels, labels)

    # Caluclate the measures and print them out
    accuracy = calculate_accuracy(conf_matrix)  # aka hit rate
    precisions = calculate_precisions(conf_matrix)
    recalls = calculate_recalls(conf_matrix)
    f1 = calculate_f1_measures(precisions, recalls)

    top_n_accuracy = calculate_top_n_accuracy()

    print(f"Accuracy : {accuracy}")
    print(f'{"Percisions per class":22}: {precisions}')
    print(f'{"Recalls per class":22}: {recalls}')
    print(f'{"F1-measures per class":22}: {f1}')

    print(f'{"Top-n accuracy":22}: {top_n_accuracy}')

    return accuracy, precisions, recalls, f1, top_n_accuracy


if __name__ == "__main__":
    path_to_csv = "evaluation/teacher_ben.csv"
    query = """
I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16. 
In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare. 
Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.

I bring to the table experience working with early teenagers, a strong background in math and computer programming, and a six-year focus on STEM subjects. 
I am personable and adept at handling workplace conflicts.

Ideally, I am looking for a school close to public transport, with positive reviews, possibly an Ofsted-rated institution. 
A reasonably good pay scale would be a welcome addition to the overall package.
    """

    # create_collection(EVAL_COLLECTION_NAME)
    evaluate(path_to_csv, query)
