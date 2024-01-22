import sqlite3

from csv import reader

job_listing_db = "job_listing.db"


def create_table(connection):
    cursor = connection.cursor()

    # Create Job Listings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            link TEXT
        )
    ''')
    connection.commit()


# ======== HELPER FUNC ============
def create_job_listing(connection, title, company, location, description, link):
    cursor = connection.cursor()

    # Returns the id of the new job listing created
    cursor.execute('''
            INSERT INTO job_listings (title, company, location, description, link)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, company, location, description, link))
    connection.commit()

    return find_job(connection, {'title': title, 'company': company, 'location': location, 'description': description, 'link': link})[0][0]


def read_job_listings(connection):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM job_listings')
    rows = cursor.fetchall()
    return rows


def update_job_listing(connection, job_id, title, company, location, description, link):
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE job_listings
        SET title=?, company=?, location=?, description=?, link=?
        WHERE id=?
    ''', (title, company, location, description, link, job_id))
    connection.commit()


def find_job(connection, criteria):
    # Example: criteria can be a dictionary like {'title': 'Software Engineer', 'location': 'CityA'}
    cursor = connection.cursor()

    query = 'SELECT * FROM job_listings WHERE '
    conditions = [f"{key}=? " for key in criteria.keys()]
    query += ' AND '.join(conditions)
    cursor.execute(query, tuple(criteria.values()))
    rows = cursor.fetchall()
    return rows


def delete_job_listing(connection, job_id):
    cursor = connection.cursor()

    cursor.execute('DELETE FROM job_listings WHERE id=?', (job_id,))
    connection.commit()


def reset_table(connection):
    cursor = connection.cursor()

    cursor.execute('DELETE FROM job_listings;')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="job_listings";')
    connection.commit()


def bulk_delete_job_listing(connection, job_ids):
    cursor = connection.cursor()

    placeholders = ','.join(['?'] * len(job_ids))
    cursor.execute(
        f"DELETE FROM job_listings WHERE id IN ({placeholders})", job_ids)
    connection.commit()


# ========= TEST DATA ==========
def populate_dummy_job_listing():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    create_job_listing(connection, "Software Engineering", "Joe inc.",
                       "London", "This is a Software Engineering job.", "www.joeinc.com")
    create_job_listing(connection, "Receptionist", "Frechclinic", "London",
                       "You will be a receptionist at our clinic.", "aaaa.uk")
    create_job_listing(connection, "Python Developer", "Snake & co.", "remote",
                       "We are looking for a python developer. We can offer a competetive salary", "python.org")
    create_job_listing(connection, "Volunteer", "Helpmeplz",
                       "london", "Charity worker needed.", "helpme.plz")
    create_job_listing(connection, "Dog sitter", "doglovr", "Manchester",
                       "Dog sitter job in Manchester", "doglvr.com")

    connection.close()


def delete_dummy_job_listing():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    delete_job_listing(connection, 1)
    delete_job_listing(connection, 2)
    delete_job_listing(connection, 3)
    delete_job_listing(connection, 4)
    delete_job_listing(connection, 5)

    connection.close()


def test_job_listing_database():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    # reset_table(connection)
    # populate_dummy_job_listing()
    # print(read_job_listings(connection))
    # print(read_job_listings())
    # delete_dummy_job_listing()
    # bulk_delete_job_listing(connection, list(range(81, 111)))

    for job in read_job_listings(connection):
        print(job)

    connection.close()


test_job_listing_database()
