from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("edit/<str:name>", views.edit, name="edit")
]
