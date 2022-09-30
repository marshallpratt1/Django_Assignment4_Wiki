from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("wiki/entry", views.entry, name="entry")
]
