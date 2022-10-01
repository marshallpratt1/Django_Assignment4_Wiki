from multiprocessing import context
from django.shortcuts import render

from . import util


def index(request):
    if request.GET:
        if request.GET["search_query"]:
            query = request.GET["search_query"].lower()
            entries = util.list_entries().lower()
            print(entries)
            if query in entries:
                return render(request, "encyclopedia/entry.html", )
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_page(request):
    pass


def wiki_entry(request, title):    
    target_entry = title
    if target_entry not in util.list_entries():
        return render(request, "encyclopedia/search.html")
    content = util.get_entry(title)
    context = {
        "entry" : target_entry,
        "content" : content,
    }
    return render(request, "encyclopedia/entry.html", context,)
