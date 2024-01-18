import sqlite3

job_listing_db = "job_listing.db"

# Connect to SQLite database (or create it if not exists)
connection = sqlite3.connect(job_listing_db)

# Create cursor to execute the sql commands
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

# Save changes to the database and close connection
connection.commit()


def create_job_listing(title, company, location, description):
    cursor.execute('''
            INSERT INTO job_listings (title, company, location, description)
            VALUES (?, ?, ?, ?)
        ''', (title, company, location, description))
    connection.commit()

    return find_job({'title': title, 'company': company, 'location': location, 'description': description})[0][0]


def read_job_listings():
    cursor.execute('SELECT * FROM job_listings')
    rows = cursor.fetchall()
    return rows


def update_job_listing(job_id, title, company, location, description):
    cursor.execute('''
        UPDATE job_listings
        SET title=?, company=?, location=?, description=?
        WHERE id=?
    ''', (title, company, location, description, job_id))
    connection.commit()

def find_job(criteria):
    # Example: criteria can be a dictionary like {'title': 'Software Engineer', 'location': 'CityA'}
    query = 'SELECT * FROM job_listings WHERE '
    conditions = [f"{key}=? " for key in criteria.keys()]
    query += ' AND '.join(conditions)
    cursor.execute(query, tuple(criteria.values()))
    rows = cursor.fetchall()
    return rows

def delete_job_listing(job_id):
    cursor.execute('DELETE FROM job_listings WHERE id=?', (job_id,))
    connection.commit()


def populate_dummy_job_listing():
    create_job_listing("Introversion Software Placement", "Introversion Software", "remote(London)", "About Introversion Software  Introversion Software is one of the UK's most-respected and successful independent game developers and publishers. Founded in 2001 by three university students, they have gone on to create critically acclaimed video games including cult classics Uplink, DEFCON, Darwinia and Prison Architect. In Feb 2010 Introversion made its first move into the console space by releasing Darwinia+ (Darwinia & Multiwinia) for Xbox Live Arcade. Introversion have previously been voted one of the top 50 Best Games Companies in the world and their most recent release, Prison Architect, has enjoyed success whilst in early access and currently has over 2 million players.   www.introversion.co.uk facebook.com/introversionsoftware twitter.com/ivsoftware youtube.com/IVSoftware  We are looking for a skilled software engineer to assist with video-game development. We will identify a specific feature or set of features for our early-access game The Last Starship, (or within one of our currently unannounced projects) and devolve ownership of this area of the game to the Intern. The successful candidate will work closely with Introversion’s senior software engineers to develop both the creative and technical approach that will result in the final project being released publicly.  A number of potential projects will be discussed at the interview stage and there will be some flexibility for the intern to choose which topic most exits them. Examples of previous projects have included a VR mode for DEFCON, Escape Mode for Prison Architect and expansion of the Subversion City Generator (See our YouTube channel for more information).  As well as the project we expect the intern to assist with other programming tasks that are demanded by business needs")
    create_job_listing("Software Engineering Intern", "ARM", "Cambridge", "Visit https://careers.arm.com/job/cambridge/software-engineering-intern/33099/55195205952  We have a range of 3 months, 6 months and 12 months industry placements across our software teams. These opportunities are available within: Architecture Technology Group, Central Technology, Central Processing Unit, Graphics Processing Unit, Machine Learning, Productivity Engineering, Software, Systems, Developer Ecosystems, and Partner Enablement Group.   Each Groups offers a new perspective and challenge within the Software Career pathway. To find out more about each of these business groups please refer to the following document:Arm Early Careers Guide to Business Groups - Software During the application process you will be able to share your interest for a specific Business Group, or \"opt-in\" to all Groups broadening your opportunity.   We work in small to medium-sized teams with most following modern Agile principles. Engineers share ideas and add to the ideas of others, document and present their work for discussion, review and support the efforts of others, whilst sharing their findings impartially and authoritatively.  What you could be doing as a Software Intern:  Working on solutions that will make use of your existing knowledge and skills, whilst also requiring you to learn something new. This could be a new language, an internal codebase or a new API. Participating in different aspects of commercial and open-source software development, from product design and implementation to testing and support. You will have plenty of help on hand from your network as you learn Overcoming a variety of different tasks to help teams hit their targets. These may involve improving and implementing new workflows, investigating new software, helping teams with design and verification of products, and many other tasks which give to the success of these projects. Using your voice to provide knowledge, new ideas and address problems independently. Gaining from our team's expertise and support throughout your placement.  We're looking for individuals who are:  You will need to be studying towards a degree in Electronic Engineering, Computer Engineering, Computer Science or any other relevant subject. Other degree types may be considered with relevant experience.  Qualities that will help your application stand out:  Experience in at least one programming language. A real passion for computing and/or the semi-conductor industry that goes beyond your studies. Curiosity about technology outside of the classroom – personal projects, hackathons, or internships etc.A desire for writing code to provide sophisticated solutions to complex problems. Good interpersonal skills with an analytical approach. An interest in new/future technology with an open-mindset to experiment. We are very keen to hire people with a desire for programming. If you can supply links to any of your projects online, we will take the time to look through them.")

def delete_dummy_job_listing():
    # Find job listings based on criteria
    job1_criteria = {'title': 'Introversion Software Placement', 'company': 'Introversion Software'}
    job2_criteria = {'title': 'Software Engineering Intern', 'company': 'ARM'}
    found_jobs1 = find_job(job1_criteria)
    found_jobs2 = find_job(job2_criteria)

    # Check if any job was found before attempting to delete
    if found_jobs1:
        # Assume we want to delete the first job found
        job_to_delete_id = found_jobs1[0][0]
        delete_job_listing(job_to_delete_id)
    else:
        print("DIDNT FIND DUMMY AAA")

    if found_jobs2:
        # Assume we want to delete the first job found
        job_to_delete_id = found_jobs2[0][0]
        delete_job_listing(job_to_delete_id)
    else:
        print("DIDNT FIND DUMMY AAA")


def test_job_listing_database():
    populate_dummy_job_listing()
    print("Data inside job listing")
    for job in read_job_listings(): print(job)

    delete_dummy_job_listing()
    print("Data without job listings")
    print(read_job_listings())


# create_job_listing("Software Engineering", "Joe inc.", "London", "This is a Software Engineering job.")
# create_job_listing("Receptionist", "Frechclinic", "London", "You will be a receptionist at our clinic.")
# create_job_listing("Python Developer", "Snake & co.", "remote", "We are looking for a python developer. We can offer a competetive salary")
# create_job_listing("Volunteer", "Helpmeplz", "london", "Charity worker needed.")
# create_job_listing("Dog sitter", "doglovr", "Manchester", "Dog sitter job in Manchester")
cursor.execute('''
        UPDATE job_listings SET 10 = 0 WHERE id = 'table_name'
    ''')

connection.commit()

print(read_job_listings())
connection.close()