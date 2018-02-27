from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', login_required(views.SearchView.as_view()), name='search'),
]