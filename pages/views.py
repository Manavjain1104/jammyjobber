from django.shortcuts import render
from django.http import HttpResponse
from semadb_utils import *
from embeddings_utils import *
from .models import Job

# Create your views here.
def home_page_view(request):
    jobs = ["This is a Software Engineering job.", "You will be a receptionist at our clinic.",
            "We are looking for a python developer. We can offer a competetive salary", "Charity worker needed.",
            "Dog sitter job in Manchester"]

    if 'query' in request.GET:
        query = request.GET['query']

        request_embedding = create_embedding(query)
        closest = search_points("testJobs", request_embedding, 2)
        job_list = [jobs[i] for i in closest]

    else:

        job_list = jobs

    return render(request, 'pages/home_search.html', {'job_list': job_list})
    # return render(request, "pages/home_search.html", {})


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
