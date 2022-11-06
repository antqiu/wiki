from django.shortcuts import render
from . import util
from random import *
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, name):
    if request.method == "POST":
        util.save_entry(name, request.POST.get("content"))
    if util.get_entry(name) is None:
        return render(request, "encyclopedia/wiki.html", {
            "entry": name.capitalize() + " not found",
            "error": True
        })
    return render(request, "encyclopedia/wiki.html", {
        "entry": markdowner.convert(util.get_entry(name)),
        "title": name.casefold()
    })


def edit(request, name):
    print("The entry that we're dealing with is " + name)
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(name),
        "name": name.casefold()
    })


def random(request):
    name = util.list_entries()[randrange(0, len(util.list_entries()))]
    return wiki(request, name)


class NewEntry(forms.Form):
    title = forms.CharField(label="title", min_length=1, max_length=50)

    content = forms.CharField(label="content", min_length=1)


def new(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return wiki(request, title)
            elif util.get_entry(title) is not None:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": "Entry already exists"
                })
    return render(request, "encyclopedia/new.html")


def search(request):
    entry = []
    string = request.POST.get("q").casefold()
    for title in util.list_entries():
        if title.casefold() == string:
            return render(request, "encyclopedia/wiki.html", {
                "entry": markdowner.convert(util.get_entry(string)),
                "title": string.casefold()
            })
        elif string.casefold() in title.casefold():
            entry.append(title)
    return render(request, "encyclopedia/search.html", {
        "entry": entry,
        "search": string.casefold()
    })
