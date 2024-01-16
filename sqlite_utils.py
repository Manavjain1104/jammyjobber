import sqlite3

connection = sqlite3.connect("job_listing.db")
connection.close()


def get_num_rows_changed_since_connection(connection):
    return connection.total_changes


def create_table(connection):
    # Create cursor to execute the sql commands
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER, name TEXT, age INTEGER)")

    # Add dummy data
    cursor.execute("INSERT INTO example VALUES (1, alice, 20)")
    cursor.execute("INSERT INTO example VALUES (2, 'bob', 30)")
    cursor.execute("INSERT INTO example VALUES (3, 'eve', 40)")

    # Save changes to the database
    connection.commit()


def read_table(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM example")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def delete_data(connection, id):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM example WHERE id = {id}")


def modify_data(connection):
    cursor = connection.cursor()
    cursor.execute("UPDATE example SET age = 31 WHERE id = 2")