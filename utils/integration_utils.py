import sqlite3
from sqlite_utils import job_listing_db, reset_table, create_job_listing
from llm_utils import create_summary, MIN_LEN, bulk_create_embeddings
from semadb_utils import bulk_add_points, COLLECTION_NAME
from csv import reader
import os
import requests
import json

# ====== CSV integration =======


def csv_into_database(collection, path_to_file, csv_delimiter=',', use_api=False):
    """Add the csv file into the sqlite and semadb database.
    WILL DELETE THE CSV FILE (to prevent duplication in database, do not push the same entries few times)

    Args:
        path_to_file (str): path to the file
        csv_delimiter (str, optional): deliminater for the csv file. Defaults to ','.
        use_api (bool, optional): use the flask connected as api call. Defaults to False.

    Raises:
        Exception: If the header is not striclty what we want
                   If uses api, the api returns an error
    """
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    if use_api:
        url = 'http://127.0.0.1:5000/summariser'

    with open(path_to_file, 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=csv_delimiter)
        csv_header = next(csv_reader)

        if csv_header != ["title", "company", "location", "description", "link"]:
            print(csv_header)
            raise Exception(
                "csv file should contain title, company, location, description, link (order matters)")

        job_ids = []
        job_embeddings = []
        job_summaries = []

        for row in csv_reader:
            # Assuming that header goes as {title, company, location, description}
            job_id = create_job_listing(connection, *tuple(row))
            job_ids.append(job_id)

            job_summary = f"The job title is {row[0]}. The company name is {row[1]}, located at {row[2]}. {row[3]}"

            if len(job_summary) > MIN_LEN:
                if use_api:
                    data = {'text': job_summary}
                    json_data = json.dumps(data)
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(
                        url, data=json_data, headers=headers)

                    if response.status_code == 200:
                        job_summary = response.json()['summary']
                        job_embedding = response.json()['embedding']
                        job_embeddings.append(job_embedding)
                    else:
                        raise Exception(
                            f"Error: {response.status_code}, {response.json()}")
                else:
                    job_summary = create_summary(job_summary)

            job_summaries.append(job_summary)

    connection.close()

    if not use_api:
        job_embeddings = bulk_create_embeddings(job_summaries)

    print(job_ids)
    print()
    print(job_summaries)
    print()
    # print(job_embedding)

    bulk_add_points(collection, job_embeddings, job_ids)

    os.remove(path_to_file)


if __name__ == "__main__":
    csv_into_database(COLLECTION_NAME, "web_scraper/nurse.csv")
