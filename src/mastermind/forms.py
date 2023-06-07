from django import forms
from .models import CodePeg


peg_choices = tuple(
    (code_peg.name, code_peg.value)
    for code_peg in CodePeg
)


class GuessForm(forms.Form):
    first_peg = forms.ChoiceField(choices=peg_choices)
    second_peg = forms.ChoiceField(choices=peg_choices)
    third_peg = forms.ChoiceField(choices=peg_choices)
    fourth_peg = forms.ChoiceField(choices=peg_choices)
