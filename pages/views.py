from django.shortcuts import render, redirect
from utils.semadb_utils import *
from utils.llm_utils import *
from utils.sqlite_utils import *
from utils.address_utils import *
from .models import Job
from .forms import CVForm
from pdfminer.high_level import extract_text
import statistics
from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.

model_used = Model.SUMMARISER
collection_used = COLLECTION_NAME


def home_page_view(request):
    # Assuming Job model has title and description fields
    query = ""
    location_query = ""

    if "query" in request.POST and request.POST.get("query"):
        query = request.POST["query"]

    if "location_query" in request.POST and request.POST.get("location_query"):
        location_query = request.POST["location_query"]

    # TODO: extract cv query to pass in loading

    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            text = extract_text(instance.pdf.path)
            query = process_data(text, Model.SUMMARY_ONLY)
            show_suggested = True
            os.remove(instance.pdf.path)
            job_list, _ = get_similar(text, 5)
            print(job_list)

    query = json.dumps(query)

    data_to_pass = {
        "query": query,
        "location_query": location_query
    }

    print("Home page gets this information -----------")
    print(data_to_pass["query"])
    print(data_to_pass["location_query"])

    # Construct URL with parameters
    url = reverse('loading_page') + '?' + urlencode(data_to_pass)

    is_posted = request.method == "POST"
    if is_posted:
        return redirect(url)
    else:
        return render(
            request,
            "pages/home_search.html",
        )


def loading_page_view(request):
    data_to_pass = {
        "query": request.GET.get("query"),
        "location_query": request.GET.get("location_query")
    }
    print("Loading page gets this information -----------")
    print(data_to_pass["query"])
    print(data_to_pass["location_query"])

    context = {"data_to_pass": data_to_pass}
    return render(request, "pages/loading.html", context)


def results_page_view(request):
    data_passed = {
        "query": request.GET.get("query"),
        "location_query": request.GET.get("location_query")
    }
    print("Results page gets this information -----------")
    print(data_passed["query"])
    print(data_passed["location_query"])

    job_instances = get_listings()
    job_list = job_instances

    query = ""
    show_suggested = False

    if data_passed["query"]:
        query = data_passed["query"]
        job_list, _ = get_similar(query, 5)
        show_suggested = True
        print("Job_list", job_list)

    if data_passed["location_query"] != "":
        location_query = data_passed["location_query"]
        job_list = [
            job for job in job_list if is_in_region(job.location, location_query)
        ]

    if "id" in request.GET:
        id = request.GET["id"]
        job_summary = [job.description for job in job_instances if job.job_id == id][0]
        job_list, _ = get_similar(job_summary, 6)

    job_list_json = json.dumps(
        [process_data(job_list[0].description, Model.SUMMARY_ONLY)]
    )
    query = json.dumps(query)

    return render(request,
                  'pages/results_page.html',
                  {"job_list": job_list, "query": query,
                      "json_list": job_list_json, "show_suggested": show_suggested},
                  )


def get_listings():
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    jobs = read_job_listings(connection)
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


def get_similar(query, number: int):
    job_instances = get_listings()
    t = 0.73
    request_embedding = process_data(query, model=model_used)
    closest, dists = search_points(collection_used, request_embedding, number)
    job_list = [job for job in job_instances if job.job_id in closest]
    for job in job_list:
        if job.is_significant < t:
            job.significant()
    return job_list, dists


def get_siginificant_data():
    _, dist2 = get_similar("nurse", 10)
    _, dist3 = get_similar("teacher", 10)
    _, dist1 = get_similar("tech", 10)
    dist = dist1 + dist2 + dist3
    avg = statistics.mean(dist)
    return avg * 0.9
