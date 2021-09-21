
from logging import PlaceHolder
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import Markdown
from django import forms
import encyclopedia

mardowner = Markdown()

import markdown
import random

listEntry = util.list_entries()
listRelated = []

class NewSearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Wiki'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter title'}))
    content = forms.CharField(label="", widget=forms.Textarea())


def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            theQuery = form.cleaned_data["query"]
            if theQuery in listEntry:
                return HttpResponseRedirect(reverse("entry", args=[theQuery]))
            else:
                for entry in listEntry:
                    if theQuery in entry:
                        listRelated.append(entry)
                    
                length = len(listRelated)
                if length == 0 or length == 1:
                    stri = "result"
                else:
                    stri = "results"
                if listRelated == None:
                    return render(request, "encyclopedia/search.html", {
                        "entries": None,
                        "line": "Sorry there is no result for your search",
                        "form": NewSearchForm()
                    })
                else:
                    return render(request, "encyclopedia/search.html", {
                        "entries": listRelated,
                        "line": f"There are {len(listRelated)} {stri} for your search",
                        "form": NewSearchForm()
                    })

    

    
def convert(TITLE):
    entry = util.get_entry(TITLE)
    htmlFile = markdown.markdown(entry) if entry else None
    return htmlFile

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid:
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in listEntry:
                return render(request, "encyclopedia/errorCreate.html", {
                    "form": NewSearchForm()
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return render(request, "encyclopedia/create.html", {
            "form1": CreateForm(),
            "form": NewSearchForm()
        })

def entries(request, i):
    entries = convert(i)
    if i == "search":
        search(request)
        
    elif entries == None:
        return render(request, "encyclopedia/error.html", {
            "title": i,
            "form": NewSearchForm()
            })
    else:
        return render(request, "encyclopedia/entries.html", {
            "entryHTML": entries,
            "titleEntry": i,
            "form": NewSearchForm()
        })



    

