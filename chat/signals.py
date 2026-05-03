from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Profile

@receiver(user_logged_in)
def online(sender, request, user, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.is_online = True
    profile.save()

@receiver(user_logged_out)
def offline(sender, request, user, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.is_online = False
    profile.save()