from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from DjangoVue import settings
from .forms import SignUpForm
from . import models
from .tokens import account_activation_token
from django.template.loader import render_to_string
import requests


def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token, account_activation_token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')


def activation_invalid_view(request):
    return render(request, 'activation_invalid.html')


def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            print(message)
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False,)
            mail = requests.post(
		        "https://api.mailgun.net/v3/sandboxf50c09da3c1a448ca6218444da66f2f1.mailgun.org/messages",
		        auth=("api", "c9fe7686a4f1fcc9daf6269e5468f314-4b1aa784-40682657"),
		        data={"from": "Mailgun Sandbox <postmaster@sandboxf50c09da3c1a448ca6218444da66f2f1.mailgun.org>",
			        "to": user.email,
			        "subject": subject,
			        "text": message})
            print(mail)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'page_title':'Signup'})


def Login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data = User.objects.filter(user=request.user))
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                if uname and upass:
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request, user)
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm, 'page_title':'Login'})
    else:
        return HttpResponseRedirect('/login/')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        return HttpResponseRedirect('login')
    else:
        return render(request, 'activation_invalid.html')


def Profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'name': request.user, 'page_title':'Profile'})
    else:
        return HttpResponseRedirect('/login/')

def Logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return HttpResponseRedirect('/login/')

def user_logout(request):
    return render(request, 'logout.html')
