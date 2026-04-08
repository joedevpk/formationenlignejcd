from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    # colonnes affichées
    list_display = ('user', 'course', 'rating', 'created_at')

    # filtres
    list_filter = ('rating', 'created_at')

    # recherche
    search_fields = ('user__username', 'course__title')

    # tri
    ordering = ('-created_at',)