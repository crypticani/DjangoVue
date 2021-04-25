from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='user Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')