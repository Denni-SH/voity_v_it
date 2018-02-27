from django.contrib.contenttypes.models import ContentType
from apps.chat.models import ConferenceRoom, DirectRoom, Message


def join_chat(key, user):
    room = ConferenceRoom.objects.get(key=key)
    room.users.add(user)
    return True

def make_direct_context(current_user, directs, rooms):
    all_rooms = rooms
    for item in directs:
        content_type = ContentType.objects.get_for_model(DirectRoom)
        obj_id = item.pk
        message = Message.objects.filter(content_type=content_type, object_id=obj_id).last()
        if item.user1 == current_user:
            whom = item.user2
        else:
            whom = item.user1
        if message:
            all_rooms.append({'room': item,
                          'type': 'direct',
                          'message': message,
                          'time': message.timestamp,
                          'destination': whom})
        else:
            all_rooms.append({'room': item,
                          'type': 'direct',
                          'message': message,
                          'time': item.created,
                          'destination': whom})
    return all_rooms



def make_group_context(groups, rooms):
    all_rooms = rooms
    for item in groups:
        content_type = ContentType.objects.get_for_model(ConferenceRoom)
        obj_id = item.pk
        message = Message.objects.filter(content_type=content_type, object_id=obj_id).last()
        if message:
            all_rooms.append({'room': item,
                          'type': 'group',
                          'message': message,
                          'time': message.timestamp})
        else:
            all_rooms.append({'room': item,
                          'type': 'group',
                          'message': message,
                          'time': item.created})
    return all_rooms