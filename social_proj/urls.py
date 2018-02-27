"""social_proj URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from apps.user_auth import views as auth_views
from apps.index.views import EditUserInfo
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/login/',  auth_views.SignIn.as_view(), name='login'),
    url(r'^account/logup/', auth_views.SignUp.as_view(), name='register'),
    url(r'^account/logout/$', views.logout, name='logout', kwargs={'next_page': '/account/login/'}),

    url(r'dialogues/',include('apps.chat.urls')),
    url(r'search/', include('apps.search_app.urls')),
    url(r'', include('apps.index.urls')),
]
