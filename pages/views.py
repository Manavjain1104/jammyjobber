from django.shortcuts import render
from django.http import HttpResponse
from semadb_utils import *
from embeddings_utils import *

# Create your views here.
def home_page_view(request):
    return render(request, "pages/home_search.html", {})


def submitted_search_view(request):
    return render(request, "pages/submitted_search.html", {})


def my_view(request):
    return render(request, 'my_template.html')


def my_function(request):
    # Your function logic here
    jobs = ["This is a Software Engineering job.", "You will be a receptionist at our clinic.",
            "We are looking for a python developer. We can offer a competetive salary", "Charity worker needed.",
            "Dog sitter job in Manchester"]

    job = "Only London"

    request_embedding = create_embedding(job)
    closest = search_points("testJobs", request_embedding, 1)

    print(jobs[closest[0]])

    return HttpResponse("Function called successfully!")