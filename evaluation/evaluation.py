import numpy as np


# ------- HELPER --------


# ------- Evaluation --------
def confusion_matrix(true_labels, predicted_labels, labels) -> np.ndarray:
    """Creates a confusion matrix based on the true and predicted labels"""
    assert len(true_labels) == len(predicted_labels), "The number of true labels and predicted labels must be the same"

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


def calculate_hit_rate(desired_jobs, recommended_jobs):
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


def calculate_accuracy(conf_matrix):
    ...


def calculate_precisions(conf_matrix):
    ...


def calculate_recalls(conf_matrix):
    ...


def calculate_f1_measures(conf_matrix):
    ...


# ------- Matrix ---------


def evaluate(path_to_csv, query):
    """Evaluates the decision tree against the testing data,
    prints the overall accuracy, and the percision, recalls,
    and f1 measures per class

    Args:
        path_to_csv(str): path to the csv file
    """

    with open(path_to_csv, 'r') as csv_file:
        ...

    true_labels = ...
    predicted_labels = ...
    labels = ...

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

    evaluate(path_to_csv, query)
