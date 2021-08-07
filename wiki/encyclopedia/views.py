from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from random import choice
import markdown2
from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request, title):
    md = markdown2.Markdown()
    content = util.get_entry(title)
    if content is None:
        return render(request,'encyclopedia/noneEntry.html',{
            'title':title
        })
    return render(request, 'encyclopedia/entry.html',{
        'title': title,
        'content': md.convert(content)
    })

def search(request):
    query = request.GET.get('q','')
    if util.get_entry(query) is not None:
        return HttpResponseRedirect(reverse('show_entry', kwargs={
            'title' : query
        }))

    mathed = []
    for entry in util.list_entries():
        if query.upper() in entry.upper():
            mathed.append(entry)
    return render(request, 'encyclopedia/searchResult.html',{
        'query' : query,
        'entries' : mathed
    })

def create(request):
    if request.method == 'POST':
        if util.get_entry(request.POST['title']) is not None:
            return HttpResponse("This is already wirted")

        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('show_entry', kwargs={
                'title':title
            }))

    form = NewEntryForm()
    return render(request, 'encyclopedia/create.html',{
        'form' : form
    })

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return HttpResponseRedirect(reverse('show_entry', kwargs={
        'title':title
    }))

def edit(request,title):
    if request.method == 'POST':
        content = request.POST['editedContent']
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('show_entry', kwargs={
            "title":title
        }))

    form = NewEntryForm()
    md = markdown2.Markdown()
    content = util.get_entry(title)
    return render(request, 'encyclopedia/edit.html',{
        'title' : title,
        'content': md.convert(content),
        'form' : form
    })
