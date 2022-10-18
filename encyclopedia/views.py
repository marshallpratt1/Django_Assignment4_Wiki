from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import messages
import markdown2, random
from . import util
from .forms import EntryForm, NewEntry, NewTitle


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#searches current entries for a match, returns closest matches if no direct match
def search(request):
    target_entry = request.GET["search_query"]   
    # slightly easier the walking the list of entries: 
    # if util.get_content(title) != None: ... 
    for entry in util.list_entries():
        if target_entry.lower() == entry.lower():
            target_entry = entry
            return redirect("/wiki/"+target_entry)
    entries = []
    for entry in util.list_entries():
        if target_entry.lower() in entry.lower() or entry.lower() in target_entry.lower():
            # very nice!
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
    if request.method == "POST": #update existing entry
        form = EntryForm(request.POST)
        new_content = ""
        if form.is_valid():
            new_content = form.cleaned_data["entry_content"]
        util.save_entry(title, new_content)
        return redirect("/wiki/"+title)
        # better done as: return redirect('wiki', title=title). subtle difference, but 
        # if there are multiple args, your way locks you into the URL structure e.g., /wiki/<str:entry>/<str:category>
    else:
        if title in util.list_entries():
            content = util.get_entry(title)
        else: 
            content = ""
        entry = EntryForm(initial={'entry_title': title,
                                    'entry_content': content})
        context = {
            "content" : content,
            "title" : title,
            "form": entry
        }
        return render(request, "encyclopedia/update.html", context,)

#create a new entry
def create_page(request):
    if request.method == "POST":
        
        #handle title form submit
        if 'title-submit' in request.POST: #render a entry form
            form = NewTitle(request.POST)
            if form.is_valid():
                new_title = form.cleaned_data["new_title"]
                cap_entries = util.list_entries()
                entries = []
                target = ""
                for entry in cap_entries:
                    entries.append(entry.lower())
                    if new_title.lower() == entry.lower():
                        target =  entry
                if new_title.lower() in entries:    
                    return render(request, "encyclopedia/error.html", {"entry": "/wiki/"+target})
                                                                        
            entry_form = NewEntry(initial={'new_title': new_title})
            context = {
                    "form": entry_form, 
                    "title": new_title,
                    }
            return render(request, "encyclopedia/create_page.html", context)
        
        #handle creating entry and render the new entry page
        if 'entry-submit' in request.POST:
            print("In entry submit")
            form = NewEntry(request.POST)
            if form.is_valid():
                print("Form is valid")
                new_title = form.cleaned_data["new_title"]
                new_content = form.cleaned_data["new_content"]
                new_content = "# "+new_title+"\n"+new_content
                #  cool! until the user already starts his entry with #title :)
                util.save_entry(new_title, new_content)
                return redirect("wiki:wiki_entry",new_title)
            else : return redirect("encyclopedia/index.html")

    else: #render the title checker form
        title_form = NewTitle()
        context = {"form": title_form}
        return render(request, "encyclopedia/create_page.html", context)


#displays existing selected wiki entry
def wiki_entry(request, title):   
    target_entry = title
    if target_entry not in util.list_entries():
        # wrong - you need to redirect to index, or else the displayed page won't show anything
        # were you to rendex index.html, you'd need to pass the context of "entries": util.list_entries()
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})
    content = util.get_entry(title)
    content = markdown2.markdown(content)
    context = {
        "content" : content,
        "title" : title,
    }
    return render(request, "encyclopedia/entry.html", context,)

def error(request):
    return render(request, "encyclopedia/error.html")

"""
def error(request, context):    
    return render(request, "encyclopedia/error.html", context)
"""