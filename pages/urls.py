from django.urls import path
from .views import home_page_view, results_page_view, loading_page_view  # , submitted_search_view

urlpatterns = [
    path("", home_page_view, name="search"),
    path("results/", results_page_view, name="results_page"),
    path('loading/', loading_page_view, name='loading_page')
]

# path("search/", submitted_search_view, name="search"),
