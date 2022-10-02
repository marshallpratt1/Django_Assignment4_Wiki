from multiprocessing import context
from django.shortcuts import redirect, render
import markdown2, random
from . import util
from .forms import NewTaskForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_page(request):
    pass

#searches current entries for a match, returns closest matches if no direct match
def search(request):
    target_entry = request.GET["search_query"]    
    for entry in util.list_entries():
        if target_entry.lower() == entry.lower():
            target_entry = entry
            return redirect("/wiki/"+target_entry)
    entries = []
    for entry in util.list_entries():
        if target_entry.lower() in entry.lower() or entry.lower() in target_entry.lower():
            entries.append(entry)
    if len(entries) == 0:
        entries = None
    context = {
        "target": target_entry,
        "entries": entries,
    }       
    return render(request, "encyclopedia/search.html", context)

#gets a random entry and displays it
def random_entry(request):
    entries = util.list_entries()
    return redirect("/wiki/"+entries[random.randint(0, len(entries)-1)])


#edit an existing entry
def edit_entry(request, title):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["entry_content"]
        util.save_entry(title, new_content)
        return redirect("/wiki/"+title)

    else:
        if title not in util.list_entries():
            return render(request, "encyclopedia/index.html")
        content = util.get_entry(title)
        entry = NewTaskForm(initial={'entry_title': title,
                                    'entry_content': content})
        context = {
            "content" : content,
            "title" : title,
            "form": entry
        }
        return render(request, "encyclopedia/update.html", context,)



#displays existing selected wiki entry
def wiki_entry(request, title):   
    target_entry = title
    if target_entry not in util.list_entries():
        return render(request, "encyclopedia/index.html")
    content = util.get_entry(title)
    content = markdown2.markdown(content)
    context = {
        "content" : content,
        "title" : title,
    }
    return render(request, "encyclopedia/entry.html", context,)
