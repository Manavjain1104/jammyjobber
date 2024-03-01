import sqlite3
from sqlite_utils import job_listing_db, reset_table, create_job_listing, read_job_listings
from llm_utils import create_summary, bulk_create_embeddings
from semadb_utils import bulk_add_points, create_collection, delete_collection, get_collection, COLLECTION_NAME, EMBEDDING_SIZE
from csv import reader
from context import web_scraper
from web_scraper.scraper_gov import extract
import os
import requests
import json

# ====== CSV integration =======


def csv_into_database(collection, path_to_file, csv_delimiter=","):
    """Add the csv file into the sqlite and semadb database.
    WILL DELETE THE CSV FILE (to prevent duplication in database, do not push the same entries few times)

    Args:
        path_to_file (str): path to the file
        csv_delimiter (str, optional): deliminater for the csv file. Defaults to ','.

    Raises:
        Exception: If the header is not striclty what we want
                   If uses api, the api returns an error
    """
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    reset_table(connection)

    with open(path_to_file, "r") as csv_file:
        csv_reader = reader(csv_file, delimiter=csv_delimiter)
        csv_header = next(csv_reader)

        if csv_header != ["title", "company", "location", "description", "link"]:
            raise Exception(
                "csv file should contain title, company, location, description, link (order matters)"
            )

        job_ids = []
        job_summaries = []

        for row in csv_reader:
            print("Process job " + row[0])
            job_info = f"The job title is {row[0]}. The company name is {row[1]}, located at {row[2]}. {row[3]}"

            job_summary = create_summary(job_info)
            job_summaries.append(job_summary)

            # Assuming that header goes as {title, company, location, (description), link}
            job_id = create_job_listing(
                connection, *tuple([row[0], row[1], row[2]] +
                                   [job_summary] + [row[4]])
            )
            job_ids.append(job_id)

    connection.close()

    job_embeddings = bulk_create_embeddings(job_summaries)
    bulk_add_points(collection, job_embeddings, job_ids)

    os.remove(path_to_file)


# ========= Repopulate Database ===========
def clear_and_reset_ll_database_stuff():
    print("Resetting the sqlite")
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    reset_table(connection)
    print(len(read_job_listings(connection)))
    connection.close()

    print("Resetting semaDB")
    delete_collection(COLLECTION_NAME)
    create_collection(COLLECTION_NAME, EMBEDDING_SIZE)
    print(get_collection(COLLECTION_NAME))


def show_database_overview():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    print(len(read_job_listings(connection)))
    connection.close()
    print(get_collection(COLLECTION_NAME))


def scrap_new_database():
    # Total 1000 entries
    healthcare_url = (
        "https://findajob.dwp.gov.uk/search?cat=12&loc=86383&sb=relevance&sd=down"
    )
    extract(url=healthcare_url,
            file_name="repopulate", min_results=260)

    general_url = (
        "https://findajob.dwp.gov.uk/search?cat=19&loc=86383&sb=relevance&sd=down"
    )
    extract(url=general_url, file_name="repopulate", min_results=110)

    education_url = (
        "https://findajob.dwp.gov.uk/search?cat=27&loc=86383&sb=relevance&sd=down"
    )
    extract(url=education_url,
            file_name="repopulate", min_results=90)

    social_worker_url = (
        "https://findajob.dwp.gov.uk/search?cat=26&loc=86383&sb=relevance&sd=down"
    )
    extract(url=social_worker_url,
            file_name="repopulate", min_results=45)

    logistics_url = (
        "https://findajob.dwp.gov.uk/search?cat=16&loc=86383&sb=relevance&sd=down"
    )
    extract(url=logistics_url,
            file_name="repopulate", min_results=45)

    hospitality_url = (
        "https://findajob.dwp.gov.uk/search?cat=13&loc=86383&sb=relevance&sd=down"
    )
    extract(url=hospitality_url,
            file_name="repopulate", min_results=45)

    engineering_url = (
        "https://findajob.dwp.gov.uk/search?cat=9&loc=86383&sb=relevance&sd=down"
    )
    extract(url=engineering_url,
            file_name="repopulate", min_results=40)

    finace_url = (
        "https://findajob.dwp.gov.uk/search?cat=1&loc=86383&sb=relevance&sd=down"
    )
    extract(url=finace_url,
            file_name="repopulate", min_results=40)

    sale_url = (
        "https://findajob.dwp.gov.uk/search?cat=23&loc=86383&sb=relevance&sd=down"
    )
    extract(url=sale_url,
            file_name="repopulate", min_results=35)

    admin_url = (
        "https://findajob.dwp.gov.uk/search?cat=2&loc=86383&sb=relevance&sd=down"
    )
    extract(url=admin_url,
            file_name="repopulate", min_results=30)

    domestic_url = (
        "https://findajob.dwp.gov.uk/search?cat=7&loc=86383&sb=relevance&sd=down"
    )
    extract(url=domestic_url,
            file_name="repopulate", min_results=30)

    # -----
    social_care_url = (
        "https://findajob.dwp.gov.uk/search?cat=177&loc=86383&sb=relevance&sd=down"
    )
    extract(url=social_care_url,
            file_name="repopulate", min_results=30)

    retail_url = (
        "https://findajob.dwp.gov.uk/search?cat=22&loc=86383&sb=relevance&sd=down"
    )
    extract(url=retail_url,
            file_name="repopulate", min_results=30)

    trade_url = (
        "https://findajob.dwp.gov.uk/search?cat=28&loc=86383&sb=relevance&sd=down"
    )
    extract(url=trade_url,
            file_name="repopulate", min_results=30)

    manufacturing_url = (
        "https://findajob.dwp.gov.uk/search?cat=18&loc=86383&sb=relevance&sd=down"
    )
    extract(url=manufacturing_url,
            file_name="repopulate", min_results=30)

    hr_url = (
        "https://findajob.dwp.gov.uk/search?cat=11&loc=86383&sb=relevance&sd=down"
    )
    extract(url=hr_url,
            file_name="repopulate", min_results=30)

    maintanance_url = (
        "https://findajob.dwp.gov.uk/search?cat=17&loc=86383&sb=relevance&sd=down"
    )
    extract(url=maintanance_url,
            file_name="repopulate", min_results=20)

    customer_service_url = (
        "https://findajob.dwp.gov.uk/search?cat=6&loc=86383&sb=relevance&sd=down"
    )
    extract(url=customer_service_url,
            file_name="repopulate", min_results=15)

    scientific_url = (
        "https://findajob.dwp.gov.uk/search?cat=24&loc=86383&sb=relevance&sd=down"
    )
    extract(url=scientific_url,
            file_name="repopulate", min_results=15)

    creative_url = (
        "https://findajob.dwp.gov.uk/search?cat=5&loc=86383&sb=relevance&sd=down"
    )
    extract(url=creative_url,
            file_name="repopulate", min_results=10)


def clean_and_repopulate_database():
    # assume file name = repopulate
    print("     Scrapping new data...")
    scrap_new_database()

    print()
    print("     Resetting both database...")
    clear_and_reset_ll_database_stuff()

    print()
    print("     Populating the database...")
    csv_into_database(COLLECTION_NAME, "scraper_output/repopulate.csv")


# ======== Aggregate Database ==============
# from the semadb get the indexes of relevent job listings (prob need to change so that the number is more)
# go to sqlite find the corresponding jobs
# use group by function there to get a grouping of job title to its track
# return a
def aggregate_job_listings():
    ...


if __name__ == "__main__":
    # uncomment these to repopulate the database from scratch
    # csv_into_database(COLLECTION_NAME, "scraper_output/accountant.csv")
    # clean_and_repopulate_database()
    show_database_overview()
