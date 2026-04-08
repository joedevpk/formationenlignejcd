from subscriptions.models import Subscription
from django.utils import timezone


def has_active_subscription(user):
    """
    Vérifie si l'utilisateur a un abonnement actif et validé
    """
    return Subscription.objects.filter(
        user=user,
        status='approved',        # ✅ CORRECT
        is_active=True,
        end_date__gt=timezone.now()
    ).exists()


def user_has_access(user, course):
    """
    Vérifie si un utilisateur peut accéder à un cours

    Règles :
    - ❌ pas connecté → refus
    - ✅ admin → accès total
    - ✅ formateur → accès
    - ✅ cours gratuit → accès
    - ✅ abonnement actif → accès
    """

    if not user.is_authenticated:
        return False

    # admin
    if user.is_superuser:
        return True

    # formateur du cours
    if hasattr(course, 'instructor') and course.instructor == user:
        return True

    # cours gratuit
    if not getattr(course, 'is_premium', True):
        return True

    # abonnement
    return has_active_subscription(user)