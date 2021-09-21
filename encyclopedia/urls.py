from encyclopedia.util import list_entries
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("<str:i>", views.entries, name="entry"),
]


