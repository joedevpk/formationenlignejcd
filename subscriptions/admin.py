from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from datetime import timedelta
from .models import Subscription, Plan


# Plans
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')


# Action pour valider paiement
@admin.action(description="Valider paiement")
def validate_payment(modeladmin, request, queryset):
    for payment in queryset:
        if not payment.status:
            payment.status = True
            payment.end_date = timezone.now() + timedelta(days=payment.plan.duration_days)
            payment.is_active = True
            payment.save()


# Abonnements
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'is_active', 'end_date', 'created_at')
    list_filter = ('status', 'plan', 'is_active')
    search_fields = ('user__username',)
    readonly_fields = ('preview_proof',)
    actions = [validate_payment]

    def preview_proof(self, obj):
        if obj.proof:
            return format_html('<img src="{}" width="200"/>', obj.proof.url)
        return "Pas d'image"
    preview_proof.short_description = "Preuve paiement"