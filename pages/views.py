from django.shortcuts import render
from django.http import HttpResponse
from utils.semadb_utils import *
from utils.llm_utils import *
from utils.sqlite_utils import *
from .models import Job
from .forms import CVForm
from pdfminer.high_level import extract_text

# Create your views here.


def home_page_view(request):
    job_instances = get_listings()

    if "query" in request.GET:
        query = request.GET["query"]
        request_embedding = create_embedding(query)
        closest = search_points(COLLECTION_NAME, request_embedding, 5)
        job_list = [job for job in job_instances if job.job_id in closest]
    else:
        job_list = job_instances
    return render(request, "pages/home_search.html", {"job_list": job_list})


def add_cv_view(request):
    submitted = False
    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            job_instances = get_listings()
            text = extract_text(instance.pdf.path)
            os.remove(instance.pdf.path)
            request_embedding = create_embedding(text)
            closest = search_points(COLLECTION_NAME, request_embedding, 5)
            job_list = [job for job in job_instances if job.job_id in closest]
            return render(request, "pages/home_search.html", {"job_list": job_list})
    else:
        form = CVForm
    context = {"form": form, "submitted": submitted}
    return render(request, "pages/add_cv.html", context)


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

        request_embedding = create_embedding(query)
        closest = search_points(COLLECTION_NAME, request_embedding, 1)
        job_list = jobs[closest[0]]

    else:
        job_list = jobs

    return render(request, "pages/home_search.html", {"job_list": job_list})


def get_listings():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    cursor = connection.cursor()

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


# def submitted_search_view(request):
#     query = request.GET.get('query', '')
#
#     jobs = ["This is a Software Engineering job.", "You will be a receptionist at our clinic.",
#             "We are looking for a python developer. We can offer a competetive salary", "Charity worker needed.",
#             "Dog sitter job in Manchester"]
#
#     request_embedding = create_embedding(query)
#     closest = search_points("testJobs", request_embedding, 1)
#
#     result = jobs[closest[0]]
#
#     return render(request, "pages/submitted_search.html", {'result': result})
