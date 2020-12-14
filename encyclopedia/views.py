import random
import logging
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

md = Markdown()

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title): 
    entries = util.list_entries()
    if title in entries: 
        page = util.get_entry(title)
        page_converted = md.convert(page) 

        return render(request, "encyclopedia/entry.html", {
            'page': page_converted,
            'title': title, 
            'form': Search()
            })
    else: 
        return render(request, "encyclopedia/error.html", {
            "message": "page was not found. " ,
            "type": "not_found", 
            "form":Search(),
            "title": title        })

def edit(request, title): 
    if request.method == 'GET':
        page = util.get_entry(title)
        
        return render(request, "encyclopedia/edit.html", {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        })
    else: 
        print("here 2")
        form = Edit(request.POST)
        if form.is_valid(): 
            textarea= form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = md.convert(page)

            return render(request, "encyclopedia/entry.html", {
            'form': Search(),
            'page': page_converted,
            'title': title
        })

def create(request):
    if request.method == "POST": 
        form = Post(request.POST)
        if form.is_valid():
            print(form)
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data['textarea']
            entries = util.list_entries()

            if title in entries: 
                return render(request, "encyclopedia/error.html", {
                "form": Search(), 
                "message": "Page already exists", 
                "title": title,
                "type": "exists"
                })

            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = md.convert(page)
                return render(request, "encyclopedia/create.html", {
                    "form": Search(), 
                    'page': page_converted, 
                    "title": title
                    })
    else: 
        return render(request, "encyclopedia/create.html", {
            "form": Search(), 
            "post": Post(),
            })

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = md.convert(page)

        context = {
            'form': Search(),
            'page': page_converted,
            'title': page_random
        }

        return render(request, "encyclopedia/entry.html", context)