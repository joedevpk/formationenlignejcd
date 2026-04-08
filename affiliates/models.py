from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# 👤 Profil affilié
class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# 🔗 Parrainage
class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referred_by")
    created_at = models.DateTimeField(auto_now_add=True)


#  Commission
class Commission(models.Model):
    affiliate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commissions_earned'  #  celui qui gagne
    )

    referred_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commissions_generated'  #  celui qui a payé
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


#  Retrait
class Withdrawal(models.Model):
    STATUS = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('rejected', 'Refusé'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)