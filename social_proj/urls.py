"""social_proj URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('apps.user_auth.urls')),
]
