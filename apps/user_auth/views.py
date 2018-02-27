from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic import CreateView
from .forms import UserCreation
from .models import User


class SignUp(CreateView):
    """
    Registration view
    """
    template_name = "registration/register.html"
    model = User
    form_class = UserCreation
    success_url = "/account/login/"


class SignIn(LoginView):
    """
    Authentication view
    """
    def get_user(self):
        return self.request.user.pk

    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse('PersonalPage', kwargs={'pk': self.request.user.pk})
