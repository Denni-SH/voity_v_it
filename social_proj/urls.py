"""social_proj URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from apps.user_auth import views as proj_views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^account/login/',  proj_views.SignIn.as_view(), name='login'),
    url(r'^account/logup/', proj_views.SignUp.as_view(), name='register'),
    url(r'^account/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'', include('apps.user_auth.urls')),
]
