from multiprocessing import context
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_page(request):
    pass


def wiki_entry(request, title):    
    target_entry = title
    context = {
        "entry" : target_entry,
    }
    return render(request, "encyclopedia/entry.html", context,)
