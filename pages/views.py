from django.shortcuts import render
from utils.semadb_utils import *
from utils.llm_utils import *
from utils.sqlite_utils import *
from utils.address_utils import *
from utils.address_utils import *
from .models import Job
from .forms import CVForm
from pdfminer.high_level import extract_text


# Create your views here.

model_used = Model.SUMMARISER
collection_used = COLLECTION_NAME


def home_page_view(request):
    # Assuming Job model has title and description fields
    job_instances = get_listings()
    job_list = job_instances

    if "query" in request.GET and request.GET.get("query"):
        query = request.GET["query"]
        request_embedding = process_data(query, model=model_used)
        closest = search_points(collection_used, request_embedding, 5)
        print(closest)
        print([job.job_id for job in job_instances])
        job_list = [job for job in job_instances if job.job_id in closest]
        print("JOB LIST", job_list)

    if "location_query" in request.GET:
        location_query = request.GET["location_query"]
        job_list = [
            job for job in job_list if is_in_region(job.location, location_query)
        ]

    if "id" in request.GET:
        id = request.GET["id"]
        job_summary = [
            job.description for job in job_instances if job.job_id == id
        ][0]
        request_embedding = process_data(job_summary, model=model_used)
        closest = search_points(collection_used, request_embedding, 6)
        job_list = [job for job in job_instances if job.job_id in closest][1:]

    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            text = extract_text(instance.pdf.path)
            os.remove(instance.pdf.path)

            request_embedding = process_data(text, model=model_used)
            closest = search_points(collection_used, request_embedding, 5)
            job_list = [job for job in job_instances if job.job_id in closest]

    return render(request, "pages/home_search.html", {"job_list": job_list})


def get_listings():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)

    jobs = read_job_listings(connection)

    # Assuming Job model has title and description fields
    job_instances = [
        Job(
            job_id=job[0],
            title=job[1],
            company=job[2],
            location=job[3],
            description=job[4],
            link=job[5],
        )
        for job in jobs
    ]
    connection.close()
    return job_instances


def job_search(request):
    jobs = [
        "This is a Software Engineering job.",
        "You will be a receptionist at our clinic.",
        "We are looking for a python developer. We can offer a competetive salary",
        "Charity worker needed.",
        "Dog sitter job in Manchester",
    ]

    if "query" in request.GET:
        query = request.GET["query"]

        request_embedding = process_data(query, model_used)
        closest = search_points(collection_used, request_embedding, 1)
        job_list = jobs[closest[0]]

    else:
        job_list = jobs

    return render(request, "pages/home_search.html", {"job_list": job_list})
