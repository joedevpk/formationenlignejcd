from django.contrib import admin
from .models import Message, Notification, Profile, BlockedUser

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(BlockedUser)