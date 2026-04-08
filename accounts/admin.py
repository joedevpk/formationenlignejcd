from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # Colonnes visibles
    list_display = (
        'username',
        'email',
        'is_student',
        'is_instructor',
        'is_finance_admin',
        'is_staff'
    )

    #  Filtres
    list_filter = (
        'is_student',
        'is_instructor',
        'is_finance_admin',
        'is_staff'
    )

    #  Organisation des champs
    fieldsets = UserAdmin.fieldsets + (
        ('Rôles', {
            'fields': (
                'is_student',
                'is_instructor',
                'is_finance_admin'
            )
        }),
    )

    #  Création utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôles', {
            'fields': (
                'is_student',
                'is_instructor',
                'is_finance_admin'
            )
        }),
    )

    # (optionnel mais pro)
    search_fields = ('username', 'email')
    ordering = ('-id',)