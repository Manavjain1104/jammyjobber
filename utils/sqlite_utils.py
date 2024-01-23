import sqlite3

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
            description TEXT
        )
    ''')
    connection.commit()


# ======== HELPER FUNC ============
def create_job_listing(connection, title, company, location, description):
    cursor = connection.cursor()

    # Returns the id of the new job listing created
    cursor.execute('''
            INSERT INTO job_listings (title, company, location, description)
            VALUES (?, ?, ?, ?)
        ''', (title, company, location, description))
    connection.commit()

    return find_job(connection, {'title': title, 'company': company, 'location': location, 'description': description})[0][0]


def read_job_listings(connection):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM job_listings')
    rows = cursor.fetchall()
    return rows


def update_job_listing(connection, job_id, title, company, location, description):
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE job_listings
        SET title=?, company=?, location=?, description=?
        WHERE id=?
    ''', (title, company, location, description, job_id))
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


# ========= TEST DATA ==========
def populate_dummy_job_listing():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    create_job_listing(connection, "Software Engineering", "Joe inc.",
                       "London", "This is a Software Engineering job.")
    create_job_listing(connection, "Receptionist", "Frechclinic", "London",
                       "You will be a receptionist at our clinic.")
    create_job_listing(connection, "Python Developer", "Snake & co.", "remote",
                       "We are looking for a python developer. We can offer a competetive salary")
    create_job_listing(connection, "Volunteer", "Helpmeplz",
                       "london", "Charity worker needed.")
    create_job_listing(connection, "Dog sitter", "doglovr", "Manchester",
                       "Dog sitter job in Manchester")

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
    reset_table(connection)
    populate_dummy_job_listing()
    # print(read_job_listings())
    # delete_dummy_job_listing()
    print(read_job_listings(connection))
    connection.close()