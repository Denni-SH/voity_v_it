from django.contrib import admin
from .models import Message, DirectRoom, ConferenceRoom


admin.site.register(DirectRoom)
admin.site.register(ConferenceRoom)
admin.site.register(Message)