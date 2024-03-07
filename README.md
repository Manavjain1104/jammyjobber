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

[![JammyJobber website][images/page-jome.png]](https://jammy-jobber-0a37e91b6b51.herokuapp.com/)

Welcome to JammyJobber, the next generation of job search powered by language models! In this project, we aim to address the limitations of traditional keyword-based job search methods and provide a more effective and intuitive way for job seekers to find relevant opportunities.

### Problem Statement and Solution

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

![Evaluation](images/eval.png)

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

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.doc.ic.ac.uk/g236002114/jammyjobber.git
git branch -M master
git push -uf origin master
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.doc.ic.ac.uk/g236002114/jammyjobber/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

---

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name

Choose a self-explaining name for your project.

## Description

Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges

On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation

Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage

Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

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
