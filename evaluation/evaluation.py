from context import utils
from utils.llm_utils import create_summary, create_embedding, bulk_create_embeddings, process_data, Model
from utils.semadb_utils import search_points
from enum import Enum

ACCOUNTANT = 9
MECHANIC = 19
TEACHER = 29
NURSE = 39
DRIVER = 49
FIREFIGHTER = 59
SECURITY_GUARD = 69
MERCHANDISER = 79
BARISTA = 89
SECRETARY = 99

class Mode(Enum):
    SIMPLE = 0
    NOISY = 1
    SUMMARISER = 2
    EXTRACTOR_REQUEST = 3

model_dict = {
    Mode.SIMPLE: Model.NONE,
    Mode.NOISY: Model.NONE,
    Mode.SUMMARISER: Model.SUMMARISER,
    Mode.EXTRACTOR_REQUEST: Model.EXTRACTOR_REQUEST,
}

evaluation_collection_dict = {
    Mode.SIMPLE: "EvaluationJobs",
    Mode.NOISY: "EvalJobsNoisy",
    Mode.SUMMARISER: "EvalJobsNoisyS",
    Mode.EXTRACTOR_REQUEST: "EvalJobsNoisyQA"
}

MODE = Mode.SIMPLE
MODEL_USED = model_dict[MODE]
EVALUATION_COLLECTION = evaluation_collection_dict[MODE]

DATASET_PURE = "scraper_output/sema_db/dataset_100.csv"
DATASET_NOISY = "scraper_output/sema_db/dataset_noisy_150.csv"

QUERIES = [
    {
        "label": ACCOUNTANT,
        "job": "accountant",
        "duties": "financial record keeping",
        "skills": "finance"
    },
    {
        "label": MECHANIC,
        "job": "mechanic",
        "duties": "repairing stuff",
        "skills": "repairing"
    },
    {
        "label": TEACHER,
        "job": "teacher",
        "duties": "teaching children",
        "skills": "communicating with children"
    },
    {
        "label": NURSE,
        "job": "nurse",
        "duties": "providing medical care",
        "skills": "medicine"
    },
    {
        "label": DRIVER,
        "job": "driver",
        "duties": "driving",
        "skills": "driving"
    },
    {
        "label": FIREFIGHTER,
        "job": "firefighter",
        "duties": "putting out fires",
        "skills": "bravery"
    },
    {
        "label": SECURITY_GUARD,
        "job": "security guard",
        "duties": "protecting properties",
        "skills": "martial arts"
    },
    {
        "label": MERCHANDISER,
        "job": "merchandiser",
        "duties": "product selection and placement",
        "skills": "marketing"
    },
    {
        "label": BARISTA,
        "job": "barista",
        "duties": "preparing drinks",
        "skills": "making food and drinks"
    },
    {
        "label": SECRETARY,
        "job": "secretary",
        "duties": "organising files, scheduling appointments, answering phone calls, and managing correspondence",
        "skills": "organising, communicating with people, and writing letters and emails"
    }
]

def calculate_recall(label, query, model, labelname):
    embedding = process_data(query, model)
    ids = search_points(EVALUATION_COLLECTION, embedding)
    correct_ids = 0
    from pathlib import Path
    from csv import reader
    with open(Path("scraper_output/sema_db/dataset_noisy_150.csv"), "r") as csv_file:
        csv_reader = reader(csv_file, delimiter=",")
        csv_header = next(csv_reader)
        rows = list(csv_reader)

        if csv_header != [
            "title" ,"company" ,"location" ,"description" ,"link"
        ]:
            raise Exception(
                "csv file should contain title, company, location, description, link (order matters)"
            )
            
        for id in ids:
            if id <= label and id > label - 10:
                correct_ids += 1
            else:
                print(rows[id][0] + " was misclassified as " + labelname)
                print("Job title is " + rows[id][0] + "." + rows[id][3])
    recall = correct_ids / 10
    print("Recall for label " + str(labelname) + " : " + str(recall))
    return(recall)

def calculate_recall_simple():
    recalls = map(lambda query: calculate_recall(query["label"], "I want to be a " + query["job"] + ".", MODEL_USED, query["job"]), QUERIES)
    avg = sum(recalls) / len(QUERIES)
    return avg

def calculate_recall_teacher():
    return calculate_recall(TEACHER, """
    I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16. 
    In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare. 
    Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
    I bring to the table experience working with early teenagers, a strong background in math and computer programming, and a six-year focus on STEM subjects. 
    I am personable and adept at handling workplace conflicts.
    Ideally, I am looking for a school close to public transport, with positive reviews, possibly an Ofsted-rated institution. 
    A reasonably good pay scale would be a welcome addition to the overall package.
        """, MODEL_USED, "Teacher long query")

def calculate_recall_duties():
    recalls = map(lambda query: calculate_recall(query["label"], "I want to " + query["duties"] + ".", MODEL_USED, query["job"]), QUERIES)
    avg = sum(recalls) / len(QUERIES)
    return avg

def calculate_recall_skills():
    recalls = map(lambda query: calculate_recall(query["label"], "I am good at " + query["skills"] + ".", MODEL_USED, query["job"]), QUERIES)
    avg = sum(recalls) / len(QUERIES)
    return avg


if __name__ == "__main__":
    import sys
    recall_simple = calculate_recall_simple()
    recall_teacher = calculate_recall_teacher()
    recall_duties = calculate_recall_duties()
    recall_skills = calculate_recall_skills()
    print("Simple recall: " + str(recall_simple))
    print("Teacher recall: " + str(recall_teacher))
    print("Duties recall: " + str(recall_duties))
    print("Skills recall: " + str(recall_skills))

    