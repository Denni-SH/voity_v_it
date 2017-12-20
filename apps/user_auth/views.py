from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import UserCreation
from .models import User
from django import forms
def hello(request):
    return render(request, 'user_auth/index.html')


class SignUp(CreateView):
    template_name = "registration/register.html"
    model = User
    form_class = UserCreation
    success_url = "/"


class SignIn(LoginView):
    template_name = 'registration/login.html'

