import sqlite3
from uuid import uuid4
from pages.models import Job

job_listing_db = "job_listing.db"


def create_table(connection):
    cursor = connection.cursor()

    # Create Job Listings table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_listings (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            link TEXT
        )
    """
    )
    connection.commit()


# ======== HELPER FUNC ============
def create_job_listing(connection, title, company, location, description, link):
    cursor = connection.cursor()

    new_uuid = str(uuid4())

    # Returns the id of the new job listing created
    cursor.execute(
        """
            INSERT INTO job_listings (id, title, company, location, description, link)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (new_uuid, title, company, location, description, link),
    )
    connection.commit()

    return new_uuid


def read_job_listings(connection):
    """Return list of tuples of all the entries"""
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM job_listings")
    rows = cursor.fetchall()
    return rows


def update_job_listing(connection, job_id, title, company, location, description, link):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_listings
        SET title=?, company=?, location=?, description=?, link=?
        WHERE id=?
    """,
        (title, company, location, description, link, job_id),
    )
    connection.commit()


def find_job(connection, criteria):
    """Find the job entries based on the criteria given

    Args:
        connection (sqlite3.connection): connection to the database
        criteria ({header: info}): dictionary of the criterias (ex. {'title': 'Software Engineer', 'location': 'CityA'})

    Returns:
        [tuples]: list of entries corresponding to the entries
    """
    cursor = connection.cursor()

    query = "SELECT * FROM job_listings WHERE "
    conditions = [f"{key}=? " for key in criteria.keys()]
    query += " AND ".join(conditions)
    cursor.execute(query, tuple(criteria.values()))
    rows = cursor.fetchall()
    return rows


def delete_job_listing(connection, job_id):
    """Delete entry corresponding to job id

    Args:
        connection (sqlite3.connection): connection to the database
        job_id (int): job id in the database
    """
    cursor = connection.cursor()

    cursor.execute("DELETE FROM job_listings WHERE id=?", (job_id,))
    connection.commit()


def reset_table(connection):
    """Clear the entries and reset the counter"""
    cursor = connection.cursor()

    cursor.execute("DELETE FROM job_listings;")
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="job_listings";')
    connection.commit()


def delete_table(connection):
    """Hard delete the table"""
    cursor = connection.cursor()

    cursor.execute("DROP TABLE job_listings;")
    connection.commit()


def bulk_delete_job_listing(connection, job_ids):
    cursor = connection.cursor()

    placeholders = ",".join(["?"] * len(job_ids))
    cursor.execute(
        f"DELETE FROM job_listings WHERE id IN ({placeholders})", job_ids)
    connection.commit()


# ========= SEARCH TITLE =========
def group_by_job_title(connection, idx=[], use_logic=False):
    # Group by the job title (associated with the indexes), if empty return all
    cursor = connection.cursor()

    # Prepare a comma-separated list of placeholders for the SQL query
    placeholders = ",".join("?" * len(idx))

    if idx == []:
        cursor.execute(
            "SELECT id, title, company, location, description, link FROM job_listings")
    else:
        cursor.execute(
            f"SELECT id, title, company, location, description, link FROM job_listings WHERE id IN ({placeholders})",
            idx
        )
    job_listings = cursor.fetchall()

    grouped_jobs = {}
    for job in job_listings:
        job_id, title, company, location, description, link = job
        if use_logic:
            matched = False
            for existing_title in grouped_jobs.keys():
                if _are_titles_related(title, existing_title):
                    grouped_jobs[existing_title].append(Job(
                        job_id=job_id,
                        title=title,
                        company=company,
                        location=location,
                        description=description,
                        link=link
                    ))
                    matched = True
                    break
            if not matched:
                grouped_jobs[title] = [Job(
                    job_id=job_id,
                    title=title,
                    company=company,
                    location=location,
                    description=description,
                    link=link
                )]
        else:
            if title not in grouped_jobs:
                grouped_jobs[title] = []
            grouped_jobs[title].append(Job(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                description=description,
                link=link
            ))
    return grouped_jobs


def _are_titles_related(title1, title2):
    # Convert both titles to lowercase for case-insensitive comparison
    title1_lower = title1.lower()
    title2_lower = title2.lower()

    # Split titles into words and find common keywords
    words1 = title1_lower.split()
    words2 = title2_lower.split()
    common_keywords = set(words1) & set(words2)

    # Check if there are common keywords between titles
    if common_keywords:
        return True

    return False
# ========= TEST DATA ==========


def populate_dummy_job_listing(connection):
    create_job_listing(
        connection,
        "Software Engineering",
        "Joe inc.",
        "London",
        "This is a Software Engineering job.",
        "www.joeinc.com",
    )
    create_job_listing(
        connection,
        "Receptionist",
        "Frechclinic",
        "London",
        "You will be a receptionist at our clinic.",
        "aaaa.uk",
    )
    create_job_listing(
        connection,
        "Python Developer",
        "Snake & co.",
        "remote",
        "We are looking for a python developer. We can offer a competetive salary",
        "python.org",
    )
    create_job_listing(
        connection,
        "Volunteer",
        "Helpmeplz",
        "london",
        "Charity worker needed.",
        "helpme.plz",
    )
    create_job_listing(
        connection,
        "Dog sitter",
        "doglovr",
        "Manchester",
        "Dog sitter job in Manchester",
        "doglvr.com",
    )


def delete_dummy_job_listing(connection):
    delete_job_listing(connection, 1)
    delete_job_listing(connection, 2)
    delete_job_listing(connection, 3)
    delete_job_listing(connection, 4)
    delete_job_listing(connection, 5)


def test_job_listing_database():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    # reset_table(connection)
    # populate_dummy_job_listing()
    # print(read_job_listings(connection))
    # print(read_job_listings())
    # delete_dummy_job_listing()
    # bulk_dele#te_job_listing(connection, list(range(111, 116)))

    for job in read_job_listings(connection):
        print(job)

    connection.close()


connection = sqlite3.connect(job_listing_db, check_same_thread=False)
# print(len(read_job_listings(connection)))
connection.close()

if __name__ == "__main__":
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    print(len(read_job_listings(connection)))
    for (i, n) in group_by_job_title(connection, use_logic=True).items():
        print(i + " " + str(len(n)))
    connection.close()
