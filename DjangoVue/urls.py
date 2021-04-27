"""DjangoVue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ProfileApp.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', Profile, name='profile'),
    path('admin/', admin.site.urls),
    path('register', signup_view, name='register'),
    path("logout", Logout, name="logout"),
    # path('user_logout', user_logout, name='user_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', Profile, name='profile'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/login',
         auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='login.html'), name='login'),
    path('invalid', activation_invalid_view, name="activation_invalid"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='login.html'),
         name='login')]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
