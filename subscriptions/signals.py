from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import SubscriptionPayment
from .models import Subscription
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=SubscriptionPayment)
def activate_subscription(sender, instance, **kwargs):

    if instance.status:

        #  éviter doublon abonnement
        if not Subscription.objects.filter(user=instance.user, is_active=True).exists():

            Subscription.objects.create(
                user=instance.user,
                plan=instance.plan,
                end_date=timezone.now() + timedelta(days=instance.plan.duration_days),
                is_active=True
            )