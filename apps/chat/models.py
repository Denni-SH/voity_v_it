from __future__ import unicode_literals
from datetime import timedelta, datetime
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.user_auth.models import User


class Room(models.Model):
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label


class DirectRoom(models.Model):
    label = models.TextField()
    user1 = models.ForeignKey(User, related_name='user1')
    user2 = models.ForeignKey(User, related_name='user2')
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class ConferenceRoom(models.Model):
    label = models.TextField()
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=60, default=1)

    def __str__(self):
        return self.label


class Message(models.Model):
    content_type = models.ForeignKey(ContentType, default=1, on_delete=models.CASCADE, null=True)
    object_id = models.IntegerField(default=1, blank=True, null=True, editable=True, verbose_name=u"room_id")

    room = GenericForeignKey('content_type', 'object_id', )
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return (self.timestamp + timedelta(hours=2)).strftime('%H:%M')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}

