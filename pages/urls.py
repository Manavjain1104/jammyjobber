from django.urls import path
from .views import home_page_view  # , submitted_search_view
from .views import add_cv_view

urlpatterns = [
    path("", home_page_view, name="home_page"),
    path("add_cv", add_cv_view, name="add-cv"),
]

# path("search/", submitted_search_view, name="search"),
