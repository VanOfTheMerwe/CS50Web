import random as rnd
import markdown2

from django.shortcuts import render, redirect
from django.urls import reverse

from . import util

# Home page view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# View to display requested wiki entry, or file-not-found error if entry is non-existent
def entry(request, title):
    page = util.get_entry(title)

    # Check if requested entry exists, if not, display error page
    if page is None:
        return render(request, "encyclopedia/not_found.html", {
            "title": title
        })

    # If entry exists, convert content to html, and render content in entry page.
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "bodyOfEntry": html
    })


# Search request
def search(request):
    if request.method == "GET":
        # Get search query
        query = request.GET["query"]

        # Check if search query matches existing entry
        if util.get_entry(query):
            return redirect(reverse('entry', args=[query]))

        # No exact entry found. Redirect to search results, with similar titles
        similar = util.get_similar(query)
        return render(request, "encyclopedia/results.html", {
            "title": query,
            "titles": similar
        })

    return redirect(reverse('index'))


# View called to redirect to a randomly chosen entry.
def random(_):
    entries = util.list_entries()
    rnd_entry = entries[rnd.randrange(0, len(entries))]

    return redirect(reverse('entry', args=[rnd_entry]))


# View to render add.html/create new entries
def add(request):
    # Render page when accessed normally
    if request.method == "GET":
        return render(request, "encyclopedia/add.html")

    # Handle creating entry when called with POST
    title = request.POST["title"]
    page = request.POST["content"]

    # Handle entry already exists
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry_already_exists.html", {
            "title": title
        })

    # Create entry
    util.save_entry(title, page)
    # and redirect to created entry
    return redirect(reverse('entry', args=[title]))


# View to render edit.html/update entries
def edit(request, title):
    # Render page when accessed normally
    if request.method == "GET":
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": page
        })

    # Otherwise, handle updating edited entry
    page = request.POST["content"]
    util.save_entry(title, page)

    # And finally, redirect to edited entry
    return redirect(reverse('entry', args=[title]))
