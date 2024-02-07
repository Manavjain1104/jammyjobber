from csv import reader
import numpy as np
from numpy.linalg import norm
from context import utils
from utils.llm_utils import create_summary, bulk_create_embeddings, process_data, Model


# ------- HELPER --------
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


def calculate_top_n_accuracy(desired_jobs, recommended_jobs, n):
    """Calculates the top n accuracy of the recommendations"""
    top_n_predictions = desired_jobs[:n]
    correct_predictions = set(
        top_n_predictions).intersection(set(recommended_jobs[:n]))
    accuracy = len(correct_predictions) / min(n, len(recommended_jobs[:n]))
    return accuracy


def calculate_error(desired_job, recommended_jobs):
    # list with the indexes from the most relevant to least
    assert (len(desired_job) == len(recommended_jobs))

    acc = 0
    not_in = 0
    for i in range(len(desired_job)):
        if (desired_job[i] in recommended_jobs):
            acc += abs(i - recommended_jobs.index(desired_job[i]))
        else:
            not_in += 1
    err = acc / len(desired_job)

    return acc  # , not_in


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

    labels = [str(dist <= dynamic_threshold).upper() for dist in distances]

    expand_distance = []
    for i in range(len(labels)):
        if labels[i] == 'TRUE':
            expand_distance.append((i, distances[i]))

    ranking = [idx for idx, _ in sorted(expand_distance, key=lambda x: x[1])]
    return labels, ranking


def add_points_to_datbase(paths_to_csv, noisy=False):
    i = 0
    for path_to_csv in paths_to_csv:
        with open(path_to_csv, 'r') as csv_file:
            csv_reader = reader(csv_file, delimiter=',')
            csv_header = next(csv_reader)

            # Check that the headers is correct
            if noisy and csv_header != ["title", "company", "location", "description", "link", 'relevant', 'keyword']:
                raise Exception(
                    "noisy csv file should contain title, company, location, description, link, relevant, keyword (order matters)")

            if not noisy and csv_header != ["title", "company", "location", "description", "link", 'relevant', 'rank', 'keyword']:
                raise Exception(
                    "csv file should contain title, company, location, description, link, relevant, rank, keyword (order matters)")

            true_labels = []
            job_summaries = []
            true_ranking = []
            keywords = []
            keyword_labels = []

            keyword_idx = 7 if not noisy else 6

            # Populate the semaDB (we do not need to create the sqlite)
            for row in csv_reader:
                if row[5] == 'TRUE' and not noisy:
                    true_ranking.append((i, row[6]))
                true_labels.append(row[5] if row[5] ==
                                   'TRUE' else 'FALSE')  # true or false

                # handle keyword value
                if int(row[keyword_idx]) > 0:
                    keyword_labels.append("TRUE")
                    keywords.append((i, row[keyword_idx]))
                else:
                    keyword_labels.append("FALSE")

                # Assuming that header start as {title, company, location, description}
                job_summary = f"The job title is {row[0]}. The company name is {row[1]}, located at {row[2]}. {row[3]}"

                if len(job_summary) > MIN_LEN:
                    job_summary = create_summary(job_summary)
                job_summaries.append(job_summary)
                i += 1

    job_embeddings = bulk_create_embeddings(job_summaries)

    true_ranking = [idx for idx, _ in sorted(
        true_ranking, key=lambda x: int(x[1]))]

    keyword_ranking = [idx for idx, _ in sorted(
        keywords, key=lambda x: int(x[1]))]

    return true_labels, true_ranking, keyword_labels, keyword_ranking, job_summaries, job_embeddings


def evaluate(paths_to_csv, query, model, noisy=False):
    """Evaluates the decision tree against the testing data,
    prints the overall accuracy, and the percision, recalls,
    and f1 measures per class

    Args:
        paths_to_csv(lst): path to the csv file
    """
    # In case the information in collection needs to be flushed

    # Process the csv and extract the jobs and qualifications
    true_labels, true_ranking, keywords_labels, keyword_ranking, job_summaries, job_embeddings = add_points_to_datbase(
        paths_to_csv, noisy)

    # Process query into embeddings
    request_embedding = process_data(query, model)

    if model != Model.KEYWORD:
        distances = [cosine_dist(request_embedding, entry_embedding)
                     for entry_embedding in job_embeddings]  # in order

        n = true_labels.count("TRUE")  # should get number of true
        distance_cut_off = sorted(distances)[n-1]
        predicted_labels = [str(dist <= distance_cut_off).upper()
                            for dist in distances]
        expand_distance = []
        for i in range(len(predicted_labels)):
            if predicted_labels[i] == 'TRUE':
                expand_distance.append((i, distances[i]))
        predicted_ranking = [idx for idx, _ in sorted(
            expand_distance, key=lambda x: x[1])]
    else:
        predicted_ranking = keyword_ranking
        predicted_labels = keywords_labels

    print(true_ranking)
    print(predicted_ranking)
    print()
    labels = ["TRUE", "FALSE"]

    # Create a confusion matrix based on the labels
    conf_matrix = confusion_matrix(
        true_labels, predicted_labels, labels)

    # Caluclate the measures and print them out
    accuracy = calculate_accuracy(conf_matrix)  # aka hit rate

    precisions = 0
    recalls = 0
    f1 = 0
    errors = 0
    top_n_accuracy = 0

    if not noisy:
        precisions = calculate_precisions(conf_matrix)
        recalls = calculate_recalls(conf_matrix)
        f1 = calculate_f1_measures(conf_matrix)
        errors = calculate_error(true_ranking, predicted_ranking)
        top_n_accuracy = calculate_top_n_accuracy(
            true_ranking, predicted_ranking, 10)

    print()
    print(f"Accuracy : {accuracy}")

    if not noisy:
        print(f'{"Percisions per class":22}: {precisions}')
        print(f'{"Recalls per class":22}: {recalls}')
        print(f'{"F1-measures per class":22}: {f1}')
        print(f'{"Top-n accuracy":22}: {top_n_accuracy}')
        print(f'{"Error":22}: {errors}')

    # TODO: KEYWORD SEARCH

    return accuracy, precisions, recalls, f1, top_n_accuracy


def evaluate_many(paths_to_csv, query_lst, model, noisy=False):
    if len(paths_to_csv) != len(query_lst):
        raise Exception("Number of elements of both should be the same")

    for i in range(len(query_lst)):
        print("Evaluating ", paths_to_csv[i])
        wrapper_evaluate_model(model, query_lst[i], paths_to_csv[i], noisy)


def wrapper_evaluate_model(model, query, paths_to_csv, noisy=False):
    """Wrapper function to evaluate the model
    """
    accuracy, precisions, recalls, f1, top_n_accuracy = evaluate(
        paths_to_csv, query, model, noisy)

    # print(f"Accuracy : {accuracy}")
    # print(f'{"Percisions per class":22}: {precisions}')
    # print(f'{"Recalls per class":22}: {recalls}')
    # print(f'{"F1-measures per class":22}: {f1}')
    # print(f'{"Top-n accuracy":22}: {top_n_accuracy}')

    # return add_points_to_datbase(paths_to_csv)


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

    models = [Model.SUMMARISER, Model.EXTRACTOR_DESCRIPTION,
              Model.NONE, Model.KEYWORD]
    for model in models:
        print(f"========== MODEL {model} ==========\n\n")

        print("\n========== METRIC 1 ==========")
        print("3qs with signal".center(30))
        # evaluate_many([[path_to_signalA], [path_to_signalB],
        #               [path_to_signalC]], [queryA, queryB, queryC], model)

        print("\n========== METRIC 2 ==========")
        # print("3qs with noise".center(30))
        # evaluate_many([[path_to_noiseA], [path_to_noiseB], [path_to_noiseC]], [
        #              queryA, queryB, queryC], model, True)

        print("\n========== METRIC 3 ==========")
        print("3qs with mixed".center(30))
        # TODO: CHANGE HERE
        # evaluate_many([[path_to_noiseA, path_to_signalA], [path_to_noiseB, path_to_signalB], [
        #              path_to_noiseC, path_to_signalC]], [queryA, queryB, queryC], model, True)

        print("\n========== METRIC 4 ==========")
        print("extended q with signal".center(30))
        path_to_csv = "evaluation/teacher_ben.csv"

        # query = """I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16.
        # In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare.
        # Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
        # """
        query = """
        I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16. 
        In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare. 
        Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
        I bring to the table experience working with early teenagers, a strong background in math and computer programming, and a six-year focus on STEM subjects. 
        I am personable and adept at handling workplace conflicts.
        Ideally, I am looking for a school close to public transport, with positive reviews, possibly an Ofsted-rated institution. 
        A reasonably good pay scale would be a welcome addition to the overall package.
        """
        wrapper_evaluate_model(model, query, path_to_csv)
