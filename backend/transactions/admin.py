from django.contrib import admin
from .models import Transaction, DistributionCommission

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_transaction', 'montant', 'frais', 'montant_net', 'statut', 'date_transaction')
    list_filter = ('type_transaction', 'statut', 'moyen_paiement', 'date_transaction')
    search_fields = ('utilisateur__full_name', 'reference_paiement')
    readonly_fields = ('date_transaction',)

@admin.register(DistributionCommission)
class DistributionCommissionAdmin(admin.ModelAdmin):
    list_display = ('beneficiaire', 'montant', 'pourcentage', 'niveau', 'date_distribution', 'est_paye')
    list_filter = ('niveau', 'est_paye')
    search_fields = ('beneficiaire__full_name',)