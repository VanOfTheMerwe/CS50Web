from django.urls import path

from . import views

urlpatterns = [
    path("wiki/<str:title>", views.entry, name="entry"), # View Entry
    path("edit/<str:title>", views.edit, name="edit"),   # Edit Entry
    path("add", views.add, name="add"),                  # Create Entry
    path("random", views.random, name="random"),         # Random Entry
    path("search", views.search, name="search"),         # Search
    path("", views.index, name="index"),                 # Index
]
