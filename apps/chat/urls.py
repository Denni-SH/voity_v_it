"""apps/chat URL Configuration
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^new_direct/id=(?P<pk>\d+)/', login_required(views.new_direct), name='NewDirect'),
    url(r'^new_conference/', login_required(views.new_conference), name='NewConference'),
    url(r'^write/id=(?P<pk>\d+)/', login_required(views.write_message), name='WriteMessage'),
    url(r'^join/group=(?P<key>[\d\w]+)/$', login_required(views.join_to_conference), name='JoinRoom'),
    url(r'^id=(?P<pk>\d+)/', login_required(views.direct_room), name='DirectRoom'),
    url(r'^group=(?P<pk>\d+)/', login_required(views.group_room), name='GroupRoom'),
    url(r'^$', login_required(views.rooms_list), name='RoomsList'),
]
