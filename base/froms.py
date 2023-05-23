from django.forms import ModelForm, widgets
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class signupform(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"}),
        }


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {
            "host": forms.Select(attrs={"class": "form-control"}),
            "topic": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "participants": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
