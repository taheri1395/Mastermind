from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import GuessForm
from .models import MastermindPlayer, CodePeg
from uuid import uuid4
from django.conf import settings


def index(request):
    if 'id' not in request.COOKIES:
        request.COOKIES["id"] = uuid4()
    user_id = request.COOKIES["id"]

    mastermind = MastermindPlayer.get_or_create(user_id=user_id)

    if request.method == 'POST':
        form = GuessForm(request.POST)
        if form.is_valid():
            mastermind.guess(
                [
                    CodePeg(form.cleaned_data['first_peg']),
                    CodePeg(form.cleaned_data['second_peg']),
                    CodePeg(form.cleaned_data['third_peg']),
                    CodePeg(form.cleaned_data['fourth_peg'])
                ]
            )
    print(mastermind._instances)
    response = render(request, "index.jinja2", {"model": {}, "form": GuessForm()})
    response.set_cookie('id', user_id)
    return response
