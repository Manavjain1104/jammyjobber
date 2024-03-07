<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.jpeg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">JammyJobber</h3>

  <p align="center">
    Neural Network Job Search using LLM
  </p>
</div>

## About The Project

![JammyJobber website][images/page-jome.png]
![Check out the website](https://jammy-jobber-0a37e91b6b51.herokuapp.com/)

Welcome to JammyJobber, the next generation of job search powered by language models! In this project, we aim to address the limitations of traditional keyword-based job search methods and provide a more effective and intuitive way for job seekers to find relevant opportunities.

The problem with keyword job search is its reliance on exact matches, leading to missed opportunities and frustration for job seekers. Our target user is anyone frustrated with the inefficiency of traditional keyword-based job search methods and seeking a better solution.
We're leveraging the power of language models to understand the nuanced needs and preferences of job seekers, resulting in more accurate and personalized job recommendations. By embedding job postings and queries in a vector space, we can provide tailored recommendations based on skills and experience.

## Technical Implementation & Database Manegement

We preprocess and embed each job posting and query in a vector space to model similarities. Our architecture involves Python, Django, JavaScript, and RESTful APIs. We host models on a digital server and use Transformers.js for client-side processing to balance response time and accuracy.
We store job embeddings in SemaDB and metadata in SQLite databases. Keeping them separate allows for easier management and scalability, enabling us to work with multiple models simultaneously.

### Built With

- Python
- Django
- JavaScript
- RESTful APIs
- Transformers.js

## Evaluation

<img src="images/eval.png" alt="Evaluation" width="400" height="300">

We evaluated our project by comparing the results of several searches against keyword search to ensure that our search performs at least as well as searching by keywords. Additionally, we manually reviewed the results of each search to identify jobs surfaced by our search that were good matches for the query but were not found by keyword search.

#### Evaluation Queries

We created three sets of queries to assess our performance:

1. Keyword Search-Equivalent: Queries structured similarly to typical keyword searches (e.g., "I want to be a nurse").
2. Skills-Based: Queries describing the candidate's skills and qualifications (e.g., "I'm trained in providing medical care").
3. Duties-Based: Queries describing features of the desired role (e.g., "I want to look after people and provide assistance").

#### Model Comparison

We compared the performance of three different language models for processing jobs and user queries:

1. No Model: The full text is directly embedded into our vector database.
2. Summarization Model: A straightforward model that summarizes the text before embedding.
3. Question and Answer Model: We ask the model to describe the main skills and interests mentioned in the query.

### Results

Our evaluation demonstrates that our search tool performs comparably to keyword search and provides additional benefits, such as surfacing relevant jobs not found by traditional methods. With further refinement and development, our search tool has the potential to revolutionize the job search process for users.

## Getting started

To get started with JammyJobber, follow the instructions below.

### Prerequisites

TODO:

- Python (version X.X)
- Django (version X.X)
- JavaScript
- RESTful APIs
- Transformers.js

### Installation

1. Clone the repo

```sh
  TODO:
  git clone https://github.com/your_username_/Project-Name.git
```

2. Install Python packages

```sh
  pip install -r requirements.txt
```

3. Git clone the LLM server and Make them run

```sh
  TODO:
  git clone https://github.com/your_username_/Project-Name.git
```

4. Create a .env file with your secret key for

```
RAPID_API_KEY=<your rapid api key>
RAPID_API_HOST="semadb.p.rapidapi.com"
LLM_SERVER_ADDRESS=<where you host the llm server>
INFERENCE_API_TOKEN=<inference api token>
```

5. Populate the job listing into databases (SemaDB and SQLite)

```python
  python utils/integration_utils.py
```

6. Run Django server

```python
  python manage.py runserver
```

7. Visit the website

```
http://127.0.0.1:8000/
```

## Usage

JammyJobber provides a user-friendly interface for job seekers to search for relevant job opportunities based on their skills and experience.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

Show your appreciation to those who have contributed to the project.

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
