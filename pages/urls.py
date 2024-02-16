from django.urls import path
from .views import home_page_view  # , submitted_search_view

urlpatterns = [
    path("", home_page_view, name="search"),
]

# path("search/", submitted_search_view, name="search"),
