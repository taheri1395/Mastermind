from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import SimpleForm


def index(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['favorite_colors'])
    return render(request, "index.jinja2", {"form": SimpleForm()})

def submit(request):
    pass
