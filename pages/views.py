from django.shortcuts import render
from django.http import HttpResponse
from .models import Job
from utils.semadb_utils import *
from utils.embeddings_utils import *
from utils.sqlite_utils import *


# Create your views here.
def home_page_view(request):
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    cursor = connection.cursor()

    jobs = read_job_listings(connection)
    print(jobs)

    # jobs = ["This is a Software Engineering job.", "You will be a receptionist at our clinic.",
    #         "We are looking for a python developer. We can offer a competetive salary", "Charity worker needed.",
    #         "Dog sitter job in Manchester"]

    if 'query' in request.GET:
        query = request.GET['query']

        request_embedding = create_embedding(query)
        closest = search_points("testJobs", request_embedding, 2)
        job_list = [jobs[i+1][4] for i in closest]

    else:
        job_list = map(lambda x: x[4], jobs)

    connection.close()

    return render(request, 'pages/home_search.html', {'job_list': job_list})


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


def job_search(request):
    jobs = ["This is a Software Engineering job.", "You will be a receptionist at our clinic.",
            "We are looking for a python developer. We can offer a competetive salary", "Charity worker needed.",
            "Dog sitter job in Manchester"]

    if 'query' in request.GET:
        query = request.GET['query']

        request_embedding = create_embedding(query)
        closest = search_points("testJobs", request_embedding, 1)
        job_list = jobs[closest[0]]

    else:

        job_list = jobs

    return render(request, 'pages/home_search.html', {'job_list': job_list})
