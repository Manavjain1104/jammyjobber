import sqlite3
from sqlite_utils import job_listing_db, reset_table, create_job_listing
from llm_utils import create_summary, MIN_LEN, bulk_create_embeddings
from semadb_utils import bulk_add_points
from csv import reader
import os

# ====== CSV integration =======


def csv_into_database(collection, path_to_file, csv_delimiter=','):
    """Add the csv file into the sqlite and semadb database.
    WILL DELETE THE CSV FILE (to prevent duplication in database, do not push the same entries few times)

    Args:
        path_to_file (str): path to the file
        csv_delimiter (str, optional): deliminater for the csv file. Defaults to ','.

    Raises:
        Exception: If the header is not striclty what we want
    """
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    with open(path_to_file, 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=csv_delimiter)
        csv_header = next(csv_reader)

        if csv_header != ["title", "company", "location", "description"]:
            print(csv_header)
            raise Exception(
                "csv file should contain title, company, lcoation, description (order matters)")

        job_ids = []
        job_summaries = []

        for row in csv_reader:
            # Assuming that header goes as {title, company, location, description}
            job_id = create_job_listing(connection, *tuple(row))
            job_ids.append(job_id)

            job_summary = f"The job title is {row[0]}. The company name is {row[1]}, located at {row[2]}. {row[3]}"

            if len(job_summary) > MIN_LEN:
                job_summary = create_summary(job_summary)

            job_summaries.append(job_summary)

    connection.close()

    bulk_add_points(collection, bulk_create_embeddings(
        job_summaries), job_ids)

    os.remove(path_to_file)


csv_into_database("job_scraped.csv")
