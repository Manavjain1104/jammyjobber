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
from itertools import chain

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
    job_titles = {}  
    job_list = []  
    show_suggested = False
    query = ""
    
    data_passed = {
        "query": request.GET.get("query"),
        "location_query": request.GET.get("location_query")
    }

    if "id" in request.GET:
        id = request.GET["id"]
        job_instances = get_listings()
        job_summary = next((job for job in job_instances if str(job.job_id) == id), None)
        if job_summary:
            job_titles = get_similar(job_summary.description, 10)
            query = job_summary.description
            job_list = list(chain.from_iterable(job_titles.values()))
        show_suggested = True 
        template_name = 'pages/results_page.html'
    else:
        # This is for the aggregated view based on query or location_query
        if data_passed["query"]:
            query = data_passed["query"]
            job_titles = get_dictionary_job(query, 20)
            job_list = list(chain.from_iterable(job_titles.values()))
            show_suggested = True
        template_name = 'pages/results_page.html'  

    job_list_json = json.dumps([job.description for job in job_list])
    query_json = json.dumps(query)

    context = {
        "job_titles": job_titles, 
        "job_list": job_list, 
        "query": query_json,
        "json_list": job_list_json, 
        "show_suggested": show_suggested
    }

    return render(request, template_name, context)

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


def get_dictionary_job(query, number: int):
    request_embedding = process_data(query, model=model_used)

    # TODO: significant
    closest, dists = search_points(collection_used, request_embedding, number)
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    dict_job = group_by_job_title(connection, idx=closest, use_logic=True)
    connection.close()

    # go though each elem in dict to see whether it is significant and modify
    keys = list(dict_job.keys())
    for old_key in keys:
        titles = dict_job[old_key]
        from collections import defaultdict
        temp = defaultdict(int)
            
        for sub in titles:
            for wrd in sub.title.split():
                if (wrd.isalnum()):
                    temp[wrd] += 1
        
        max_cnt = max(temp.values())
        new_key = ""
        for key, value in sorted(temp.items(), key=lambda kv: kv[1], reverse=True):
            if max_cnt > value:
                break
            new_key += key + " "
            
        dict_job[new_key] = dict_job.pop(old_key)
            
    return dict_job


def get_similar(query, number: int):
    job_instances = get_listings()
    t = 0.73
    request_embedding = process_data(query, model=model_used)
    closest, dists = search_points(collection_used, request_embedding, number)
    connection = sqlite3.connect(job_listing_db, check_same_thread=False)
    dict_job = group_by_job_title(connection, idx=closest, use_logic=True)
    connection.close()

    # go though each elem in dict to see whether it is significant and modify
    keys = list(dict_job.keys())
    for old_key in keys:
        titles = dict_job[old_key]
        from collections import defaultdict
        temp = defaultdict(int)
            
        for sub in titles:
            for wrd in sub.title.split():
                if (wrd.isalnum()):
                    temp[wrd] += 1
        
        max_cnt = max(temp.values())
        new_key = ""
        for key, value in sorted(temp.items(), key=lambda kv: kv[1], reverse=True):
            if max_cnt > value:
                break
            new_key += key + " "
            
        dict_job[new_key] = dict_job.pop(old_key)
        
    for value in dict_job.values():
        for job in value:
            if job.is_significant < t:
                job.significant()          
    
    return dict_job


def get_siginificant_data():
    _, dist2 = get_similar("nurse", 10)
    _, dist3 = get_similar("teacher", 10)
    _, dist1 = get_similar("tech", 10)
    dist = dist1 + dist2 + dist3
    avg = statistics.mean(dist)
    return avg * 0.9
