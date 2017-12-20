from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    locality = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(blank=True)
    phone = models.CharField(max_length=20, blank=True)