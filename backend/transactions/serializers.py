from rest_framework import serializers
from .models import Transaction, DistributionCommission
from accounts.serializers import UserSerializer

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer pour les transactions."""
    utilisateur_details = UserSerializer(source='utilisateur', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'utilisateur', 'utilisateur_details',
            'type_transaction', 'montant', 'frais', 'montant_net',
            'moyen_paiement', 'reference_paiement', 'statut',
            'date_transaction', 'date_validation', 'description',
            'transaction_originale', 'niveau_commission'
        ]
        read_only_fields = ['id', 'date_transaction', 'frais', 'montant_net']


class DistributionCommissionSerializer(serializers.ModelSerializer):
    """Serializer pour les distributions de commission."""
    beneficiaire_details = UserSerializer(source='beneficiaire', read_only=True)
    
    class Meta:
        model = DistributionCommission
        fields = [
            'id', 'transaction_source', 'beneficiaire', 'beneficiaire_details',
            'montant', 'pourcentage', 'niveau', 'date_distribution', 'est_paye'
        ]
        read_only_fields = ['id', 'date_distribution']