from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='user Name',
        widget=forms.TextInput(
            attrs={
            'class':'block appearance-none w-full bg-white border border-grey-light hover:border-grey px-2 py-2 rounded shadow',
            'placeholder':'Your Username'
            }
    ))
    email = forms.EmailField(max_length=150, help_text='Email',
        widget=forms.TextInput(
            attrs={
            'class':'block appearance-none w-full bg-white border border-grey-light hover:border-grey px-2 py-2 rounded shadow',
            'placeholder':'Your Email'
            }
    ))
    password1 = forms.CharField(max_length=30, help_text='Password',
        widget=forms.PasswordInput(
            attrs={
            'class':'block appearance-none w-full bg-white border border-grey-light hover:border-grey px-2 py-2 rounded shadow',
            'placeholder':'Password'
            }
    ))
    password2 = forms.CharField(max_length=30, help_text='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
            'class':'block appearance-none w-full bg-white border border-grey-light hover:border-grey px-2 py-2 rounded shadow',
            'placeholder':'Confirm Password'
            }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')