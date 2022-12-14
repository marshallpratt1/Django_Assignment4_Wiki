from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("wiki/create_page_content", views.create_page, name="create_page_content"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random", views.random_entry, name="random"),
    path("wiki/error", views.error, name="error"),
    path("wiki/edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("wiki/<str:title>", views.wiki_entry, name="wiki_entry"),
]
