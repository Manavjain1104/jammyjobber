from django.shortcuts import render


# Create your views here.
def home_page_view(request):
    return render(request, "pages/home_search.html", {})


def submitted_search_view(request):
    return render(request, "pages/submitted_search.html", {})
