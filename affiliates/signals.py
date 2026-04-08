from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Affiliate

User = get_user_model()

@receiver(post_save, sender=User)
def create_affiliate(sender, instance, created, **kwargs):
    if created:
        Affiliate.objects.create(user=instance)