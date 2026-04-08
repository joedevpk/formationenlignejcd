from django.contrib import admin
from .models import Notification
from django.contrib.auth import get_user_model
from .utils import send_notification  #  important

User = get_user_model()


#  ACTION : marquer comme lu
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)

mark_as_read.short_description = "Marquer comme lu"


#  ACTION : envoyer à tous les utilisateurs (TEMPS RÉEL)
def send_to_all_users(modeladmin, request, queryset):
    users = User.objects.all()

    for notif in queryset:
        for user in users:
            send_notification(  #  au lieu de create()
                user,
                notif.message
            )

send_to_all_users.short_description = "Envoyer à tous les utilisateurs"


#  ACTION : envoyer aux abonnés
def send_to_subscribers(modeladmin, request, queryset):

    #  adapte selon ton système abonnement
   # Subscription.objects.filter(active=True)
    users = User.objects.filter(is_active=True)

    for notif in queryset:
        for user in users:
            send_notification(
                user,
                notif.message
            )

send_to_subscribers.short_description = "Envoyer aux abonnés"


#  ADMIN PRINCIPAL
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    #  colonnes affichées
    list_display = ('user', 'short_message', 'is_read', 'created_at')

    #  filtres
    list_filter = ('is_read', 'created_at')

    #  recherche
    search_fields = ('message', 'user__username')

    #  tri
    ordering = ('-created_at',)

    #  édition rapide
    list_editable = ('is_read',)

    #  actions admin
    actions = [
        mark_as_read,
        send_to_all_users,
        send_to_subscribers
    ]

    #  afficher message court (UI propre)
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message"