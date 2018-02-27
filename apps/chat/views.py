from operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from .utils import join_chat, make_direct_context, make_group_context
from .models import ConferenceRoom, DirectRoom, Message
from apps.user_auth.models import User
import uuid

@login_required
def new_direct(request, pk):
    """
    Creating new direct room view
    """
    whom = User.objects.get(pk=pk)
    new_room = DirectRoom.objects.create(user1=request.user, user2=whom)
    return redirect(direct_room, pk=new_room.pk)

@login_required
def new_conference(request):
    """
    Creating new group room view
    """
    key = str(uuid.uuid4()).replace("-", "")
    new_room = ConferenceRoom.objects.create(key=key)
    new_room.label = new_room.pk
    new_room.save()
    return redirect(join_to_conference, key=new_room.key)

@login_required
def group_room(request, pk):
    """
    Group room view
    """
    room, created = ConferenceRoom.objects.get_or_create(pk=pk)
    handlers_list = [item.username for item in room.users.all()]
    if request.user.username not in handlers_list:
        return redirect('/')
    content_type = ContentType.objects.get_for_model(ConferenceRoom)
    obj_id = room.pk

    # show the last 50 messages, ordered most-recent-last
    messages = reversed(Message.objects.filter(content_type=content_type, object_id=obj_id).order_by('-timestamp')[:50])
    return render(request, "room.html", {
        'room': room,
        'messages': messages,
        'type': 'group'
    })

@login_required
def direct_room(request, pk):
    """
    Direct room view
    """
    room, created = DirectRoom.objects.get_or_create(pk=pk)
    content_type = ContentType.objects.get_for_model(DirectRoom)
    obj_id = room.pk
    if room.user1 == request.user:
        whom = User.objects.get(pk=room.user2.pk)
    else:
        whom = User.objects.get(pk=room.user1.pk)

    # check user permission on this room
    if room.user1 != request.user and room.user2 != request.user:
        return redirect('/')

    # show the last 50 messages, ordered most-recent-last
    messages = reversed(Message.objects.filter(content_type=content_type, object_id=obj_id).order_by('-timestamp')[:50])
    return render(request, "room.html", {
        'room': room,
        'messages': messages,
        'type': 'direct',
        'destination': whom
    })

@login_required
def rooms_list(request):
    """
    Room list view
    """
    directs = DirectRoom.objects.filter(user1=request.user) | DirectRoom.objects.filter(user2=request.user)
    groups = ConferenceRoom.objects.filter(users=request.user)
    current_user = request.user
    rooms = []
    rooms = make_direct_context(current_user, directs, rooms)
    rooms = make_group_context(groups, rooms)
    sort_rooms = sorted(rooms, key=itemgetter('time'))
    users = User.objects.all()
    return render(request, 'chat_list.html', {
        'groups': groups,
        'directs': directs,
        'rooms':reversed(sort_rooms),
        'users': users
    })

@login_required
def join_to_conference(request, key):
    """
    Join to group room view
    """
    join_chat(key, request.user)
    room = ConferenceRoom.objects.get(key=key)
    return redirect(group_room, pk=room.pk)

@login_required
def write_message(request, pk):
    """
    Redirect to direct view
    """
    who = request.user
    whom = User.objects.get(pk=pk)
    if DirectRoom.objects.filter(user1=who, user2=whom).exists():
        room = DirectRoom.objects.get(user1=who, user2=whom)
    elif DirectRoom.objects.filter(user1=whom, user2=who).exists():
        room = DirectRoom.objects.get(user1=whom, user2=who)
    else:
        return redirect(new_direct, pk=pk)
    return redirect(direct_room, pk=room.pk)
