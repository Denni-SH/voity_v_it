import json
import logging
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from django.contrib.contenttypes.models import ContentType
from .models import ConferenceRoom, Message, DirectRoom

log = logging.getLogger(__name__)

@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    try:
        prefix, label = message['path'].strip('/').split('/')
        room_type, room_pk = label.strip(' ').split('=')
        if prefix != 'dialogues':
            log.debug('invalid ws path=%s', message['path'])
            return
        if room_type == 'group':
            room = ConferenceRoom.objects.get(pk=room_pk)
        elif room_type == 'id':
            room = DirectRoom.objects.get(pk=room_pk)
        else:
            log.debug('invalid room type=%s', room_type)
            # print('!!!!!!!!!!!!!!!!OPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            return
    except ValueError:
        # print('invalid ws path=%s', message['path'])
        log.debug('invalid ws path=%s', message['path'])
        return
    except ConferenceRoom.DoesNotExist:
        log.debug('ws room does not exist label=%s', room_pk)
        return
    except DirectRoom.DoesNotExist:
        log.debug('ws room does not exist label=%s', room_pk)
        return
    log.debug('chat connect room=%s client=%s:%s',
              room.pk, message['client'][0], message['client'][1])
    Group('chat-' + str(room_pk), channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['room'] = room.pk
    message.channel_session['type'] = room_type

@channel_session_user
def ws_receive(message):
    try:
        room_pk = message.channel_session['room']
        room_type = message.channel_session['type']
        if room_type == 'group':
            room = ConferenceRoom.objects.get(pk=room_pk)
        elif room_type == 'id':
            room = DirectRoom.objects.get(pk=room_pk)
        else:
            log.debug('invalid room type=%s', room_type)
            return
    except KeyError:
        log.debug('no room in channel_session')
        return
    except ConferenceRoom.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', room_pk)
        return
    except DirectRoom.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', room_pk)
        return
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s message=%s',
                  room.label, data['message'])
        data['handle'] = message.user.first_name + ' ' + message.user.last_name
        if room_type == 'group':
            content_type = ContentType.objects.get_for_model(ConferenceRoom)
        elif room_type == 'id':
            content_type = ContentType.objects.get_for_model(DirectRoom)
        else:
            log.debug('invalid room type=%s', room_type)
            return
        obj_id = room.pk
        cur_message = Message.objects.create(handle=data['handle'],
                                             message=data['message'],
                                             content_type=content_type,
                                             object_id=obj_id)

        Group('chat-' + str(room_pk), channel_layer=message.channel_layer).send({'text': json.dumps(cur_message.as_dict())})

@channel_session_user
def ws_disconnect(message):
    try:
        room_pk = message.channel_session['room']
        Group('chat-' + str(room_pk), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, ConferenceRoom.DoesNotExist):
        pass
