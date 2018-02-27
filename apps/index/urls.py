from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^settings/',
        login_required(views.EditUserInfo.as_view()),
        name='Settings'),
    url(r'^friends/actions/(?P<operation>\w+)/id=(?P<pk>\d+)/',
        login_required(views.add_or_remove_friend),
        name='AddOrRemoveFriend'),
    url(r'^friends/',
        login_required(views.FriendsList.as_view()),
        name='Friends'),
    url(r'^friend_request/(?P<operation>\w+)/id=(?P<pk>\d+)/',
        login_required(views.add_or_remove_friend_request),
        name='AddOrRemoveSubscribe'),
    url(r'^leave_in_subscribers/id=(?P<pk>\d+)/',
        login_required(views.leave_in_subscribers),
        name='LeaveInSubscribers'),
    url(r'^id=(?P<pk>\d+)/',
        views.personal_page,
        name='PersonalPage'),
    url(r'^',
        views.index,
        name='index'),
]

static(settings.STATIC_URL, document_root=settings.STATIC_URL)
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)