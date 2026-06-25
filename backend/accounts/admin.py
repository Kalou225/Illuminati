from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Champs affichés dans la liste
    list_display = ('email', 'full_name', 'phone_number', 'grade', 'is_staff', 'date_joined')
    list_filter = ('grade', 'is_staff', 'is_active')
    
    # Champs pour la recherche
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)

    # Champs affichés dans le formulaire de création/édition
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('full_name', 'phone_number', 'grade', 'sponsor', 'referral_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('date_joined',)}),
    )

    # Champs pour créer un nouvel utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'grade', 'password1', 'password2'),
        }),
    )