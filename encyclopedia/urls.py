from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("<str:entry>", views.entry, name="entry")
]
