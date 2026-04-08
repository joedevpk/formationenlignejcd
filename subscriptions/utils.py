from django.utils import timezone
from django.core.mail import send_mail
from subscriptions.models import Subscription
from io import BytesIO
import qrcode

# 🔹 Génération QR code
def generate_qr_code(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return buffer

# 🔔 Rappel automatique d'expiration
def send_expiration_reminder():
    from datetime import timedelta
    reminder_date = timezone.now() + timedelta(days=3)

    subs = Subscription.objects.filter(
        end_date__date=reminder_date.date(),
        is_active=True
    )

    for sub in subs:
        send_mail(
            "⚠️ Abonnement expire bientôt",
            f"Salut {sub.user.username}, ton abonnement expire bientôt.",
            "noreply@joedev.com",
            [sub.user.email],
            fail_silently=True
        )

# 🔑 Vérification d'accès aux cours (TOUS PREMIUM)
def user_has_access(user, course):
    """
    Vérifie si un utilisateur peut accéder au cours
    Règles :
    - ❌ Utilisateur non connecté → refus
    - ✅ Superuser/admin → accès
    - ✅ Formateur du cours → accès
    - ✅ Abonnement actif et validé → accès
    """
    if not user.is_authenticated:
        return False

    # Admin / superuser
    if getattr(user, 'is_superuser', False):
        return True

    # Formateur du cours
    if hasattr(course, 'instructor') and course.instructor == user:
        return True

    # Abonnement actif
    return Subscription.objects.filter(
        user=user,
        status=True,          # paiement validé
        is_active=True,       # abonnement actif
        end_date__gt=timezone.now()  # non expiré
    ).exists()