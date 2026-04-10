from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from cloudinary.models import CloudinaryField




User = settings.AUTH_USER_MODEL


class Plan(models.Model):
    """Plans d'abonnement: Basic / Pro / Premium"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Abonnement d'un utilisateur à un plan"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    proof = CloudinaryField('proof', blank=True, null=True)
    #proof = CloudinaryField(upload_to='proofs/', blank=True, null=True)  # capture paiement
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    STATUS_CHOICES = [
    ('pending', 'En attente'),
    ('approved', 'Validé'),
    ('rejected', 'Refusé'),
]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    #status = models.BooleanField(default=False)  # ❌ non validé / ✅ validé

    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status.capitalize()}"
        #{'Validé' if self.status else 'En attente'}"

    def save(self, *args, **kwargs):
        # Si nouvel abonnement et end_date non défini
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=self.plan.duration_days)

        # Met à jour l'état actif
        self.is_active = self.end_date > timezone.now()
        super().save(*args, **kwargs)

    def is_valid(self):
        """Retourne True si l'abonnement est actif et non expiré"""
        return self.is_active and self.end_date > timezone.now()
    






