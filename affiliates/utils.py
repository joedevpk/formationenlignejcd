from .models import Referral, Commission, Affiliate
from notifications.models import Notification

def give_commission(user, amount):
    referral = Referral.objects.filter(referred_user=user).first()

    if referral:
        # éviter double commission
        if not Commission.objects.filter(
            affiliate=referral.referrer,
            referred_user=user
        ).exists():

            commission = amount * 0.2

            Commission.objects.create(
                affiliate=referral.referrer,
                referred_user=user,
                amount=commission
            )

            affiliate = Affiliate.objects.get(user=referral.referrer)
            affiliate.balance += commission
            affiliate.save()

            # 🔔 notification
            Notification.objects.create(
                user=referral.referrer,
                message=f"🔥 Tu as gagné {commission}$"
            )