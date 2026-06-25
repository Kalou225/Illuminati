from django.contrib import admin
from .models import Loge, NiveauReferral, RelationParrainage

@admin.register(Loge)
class LogeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'grand_maitre', 'date_creation', 'est_active')
    list_filter = ('est_active',)
    search_fields = ('nom',)

@admin.register(NiveauReferral)
class NiveauReferralAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'pourcentage_commission')
    ordering = ('niveau',)

@admin.register(RelationParrainage)
class RelationParrainageAdmin(admin.ModelAdmin):
    list_display = ('parrain', 'filleul', 'niveau', 'date_parrainage', 'est_actif')
    list_filter = ('niveau', 'est_actif')
    search_fields = ('parrain__full_name', 'filleul__full_name')