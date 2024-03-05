from django import forms
from django.forms import ModelForm
from .models import CV
from taggit.forms import *


class CVForm(ModelForm):
    class Meta:
        model = CV
        fields = ("pdf",)

        widgets = {"pdf": forms.FileInput()}
