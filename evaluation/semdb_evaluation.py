from context import utils
from utils.llm_utils import create_summary, create_embedding, bulk_create_embeddings, process_data, Model
from utils.semadb_utils import search_points

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

MODEL_USED = Model.EXTRACTOR_DESCRIPTION

EVALUATION_COLLECTION_BASIC = "EvaluationJobs"
EVALUATION_COLLECTION_NOISY = "EvalJobsNoisy"
EVALUATION_COLLECTION_SUMMARISER = "EvalJobsNoisyS"
EVALUATION_COLLECTION_QA = "EvalJobsNoisyQA"

DATASET_PURE = "scraper_output/sema_db/dataset_100.csv"
DATASET_NOISY = "scraper_output/sema_db/dataset_noisy_150.csv"

def calculate_recall(label, query, model, labelname):
    embedding = process_data(query, model)
    ids = search_points(EVALUATION_COLLECTION_QA, embedding)
    correct_ids = 0
    from pathlib import Path
    from csv import reader
    with open(Path("scraper_output/sema_db/combined_file_copy.csv"), "r") as csv_file:
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

if __name__ == "__main__":
    import sys
    sys.stdout = open('output.txt','wt')
    avg = 0
    print("\n========== METRIC 1 (I want to be a...) ==========")
    avg += calculate_recall(ACCOUNTANT, "I want to be an accountant. I ", MODEL_USED, "Accountat")
    avg += calculate_recall(TEACHER, "I want to be an teacher.", MODEL_USED, "Teacher")
    avg += calculate_recall(NURSE, "I want to be an nurse.", MODEL_USED, "Nurse")
    avg += calculate_recall(DRIVER, "I want to be an driver.", MODEL_USED, "Driver")
    avg += calculate_recall(FIREFIGHTER, "I want to be a firefighter.", MODEL_USED, "Firefighter")
    avg += calculate_recall(SECURITY_GUARD, "I want to be a security guard.", MODEL_USED, "Security guard")
    avg += calculate_recall(MERCHANDISER, "I want to be a merchandiser.", MODEL_USED, "Merchandiser")
    avg += calculate_recall(SECRETARY, "I want to be a secretary.", MODEL_USED, "Secretary")
    avg += calculate_recall(BARISTA, "I want to be a barista.", MODEL_USED, "Barista")
    avg += calculate_recall(MECHANIC, "I want to be a mechanic.", MODEL_USED, "Mechanic")
    avg = avg / 10
    print("Average recall: " + str(avg))
    print("\n========== METRIC 2 (Real teacher query) ==========")
    calculate_recall(TEACHER, """
I am seeking a permanent teaching position in a secondary school in London, specializing in STEM subjects for students aged 11-16. 
In my day-to-day role, I want to teach a variety of STEM subjects (math, science, computing), attend every weekday, participate in lunch duty, and be involved in monitoring the general community behavior and welfare. 
Additionally, I aim to have time for lesson planning, marking work, and personal time in the evening.
I bring to the table experience working with early teenagers, a strong background in math and computer programming, and a six-year focus on STEM subjects. 
I am personable and adept at handling workplace conflicts.
Ideally, I am looking for a school close to public transport, with positive reviews, possibly an Ofsted-rated institution. 
A reasonably good pay scale would be a welcome addition to the overall package.
    """, MODEL_USED, "Teacher long query")
    print("\n========== METRIC 3 (I want to ... without profession mentioning) ==========")
    avg = 0
    avg += calculate_recall(ACCOUNTANT, "I want to do financial record keeping. ", MODEL_USED, "Accountat")
    avg += calculate_recall(TEACHER, "I want to teach children.", MODEL_USED, "Teacher")
    avg += calculate_recall(NURSE, "I want to provide medical care.", MODEL_USED, "Nurse")
    avg += calculate_recall(DRIVER, "I want to drive a car.", MODEL_USED, "Driver")
    avg += calculate_recall(FIREFIGHTER, "I want to put out fires.", MODEL_USED, "Firefighter")
    avg += calculate_recall(SECURITY_GUARD, "I want to protect properties.", MODEL_USED, "Security guard")
    avg += calculate_recall(MERCHANDISER, "I want to do product selection and placement.", MODEL_USED, "Merchandiser")
    avg += calculate_recall(SECRETARY, "I want to organise files, schedule appointments, answer phone calls, and manage correspondence.", MODEL_USED, "Secretary")
    avg += calculate_recall(BARISTA, "I want to prepare drinks.", MODEL_USED, "Barista")
    avg += calculate_recall(MECHANIC, "I want to repair mechanisms.", MODEL_USED, "Mechanic")
    avg = avg / 10
    print("Average recall: " + str(avg))
    
    print("\n========== METRIC 4 (I am good at ...) ==========")
    avg = 0
    avg += calculate_recall(ACCOUNTANT, "I am good at finance. ", MODEL_USED, "Accountat")
    avg += calculate_recall(TEACHER, "I am good at communicating with children.", MODEL_USED, "Teacher")
    avg += calculate_recall(NURSE, "I am good at medicine.", MODEL_USED, "Nurse")
    avg += calculate_recall(DRIVER, "I am good at driving.", MODEL_USED, "Driver")
    avg += calculate_recall(FIREFIGHTER, "I am strong physically and I am brave. I will easily rescue a person.", MODEL_USED, "Firefighter")
    avg += calculate_recall(SECURITY_GUARD, "I am strong, responsible, and know martial arts. I can protect anything and anyone.", MODEL_USED, "Security guard")
    avg += calculate_recall(MERCHANDISER, "I am good at marketing. I can predict what customers want.", MODEL_USED, "Merchandiser")
    avg += calculate_recall(SECRETARY, "I am good at organising, communicating with people, and writing letters and emails.", MODEL_USED, "Secretary")
    avg += calculate_recall(BARISTA, "I am good at making food and drinks.", MODEL_USED, "Barista")
    avg += calculate_recall(MECHANIC, "I am good at repairing stuff.", MODEL_USED, "Mechanic")
    avg = avg / 10
    print("Average recall: " + str(avg))
    
    