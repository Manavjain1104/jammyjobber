from django.shortcuts import render
from utils.semadb_utils import *
from utils.llm_utils import *
from utils.sqlite_utils import *
from utils.address_utils import *
from utils.address_utils import *
from .models import Job
from .forms import CVForm
from pdfminer.high_level import extract_text
import statistics

# Create your views here.

model_used = Model.SUMMARISER
collection_used = COLLECTION_NAME


def home_page_view(request):
    # Assuming Job model has title and description fields
    job_instances = get_listings()
    job_list = job_instances

    query = ""

    if "query" in request.GET and request.GET.get("query"):
        query = request.GET["query"]
        job_list, _ = get_similar(query, 5)
        print(job_list)

    if "location_query" in request.GET:
        location_query = request.GET["location_query"]
        job_list = [
            job for job in job_list if is_in_region(job.location, location_query)
        ]

    if "id" in request.GET:
        id = request.GET["id"]
        job_summary = [job.description for job in job_instances if job.job_id == id][0]
        job_list, _ = get_similar(job_summary, 6)

    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            text = extract_text(instance.pdf.path)
            query = text
            os.remove(instance.pdf.path)
            job_list, _ = get_similar(text, 5)
            print(job_list)

    job_list_json = json.dumps(
        [process_data(job_list[0].description, Model.SUMMARY_ONLY)]
    )
    query = json.dumps(query)

    return render(
        request,
        "pages/home_search.html",
        {"job_list": job_list, "query": query, "json_list": job_list_json},
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
            print("YESSSS")
    return job_list, dists


def get_siginificant_data():
    _, dist2 = get_similar("nurse", 10)
    _, dist3 = get_similar("teacher", 10)
    _, dist1 = get_similar("tech", 10)
    dist = dist1 + dist2 + dist3
    avg = statistics.mean(dist)
    return avg * 0.9
