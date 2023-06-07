from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import GuessForm


def index(request):
    if request.method == 'POST':
        form = GuessForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    return render(request, "index.jinja2", {"model": {}, "form": GuessForm()})
