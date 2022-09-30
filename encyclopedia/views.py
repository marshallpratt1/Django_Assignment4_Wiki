from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_page(request):
    pass


def entry(request):    
    return render(request, "encyclopedia/entry.html")