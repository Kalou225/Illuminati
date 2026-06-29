from rest_framework import serializers
from decimal import Decimal
from .models import Transaction, DistributionCommission
from .services import CommissionService
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
        read_only_fields = ['id', 'date_transaction', 'frais', 'montant_net', 'statut']


class DepotSerializer(serializers.Serializer):
    """Serializer pour créer un dépôt."""
    montant = serializers.DecimalField(max_digits=12, decimal_places=2)
    moyen_paiement = serializers.ChoiceField(choices=Transaction.MOYEN_PAIEMENT_CHOICES)
    reference_paiement = serializers.CharField(required=False, allow_blank=True)
    
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à 0.")
        return value
    
    def create(self, validated_data):
        utilisateur = self.context['request'].user
        montant = validated_data['montant']
        
        # Créer la transaction de dépôt
        depot = Transaction.objects.create(
            utilisateur=utilisateur,
            type_transaction='DEPOT',
            montant=montant,
            frais=Decimal('0.00'),
            montant_net=montant,
            moyen_paiement=validated_data['moyen_paiement'],
            reference_paiement=validated_data.get('reference_paiement', ''),
            statut='VALIDEE',
            description=f"Dépôt via {validated_data['moyen_paiement']}"
        )
        
        # Distribuer les commissions
        commissions = CommissionService.distribuer_commissions(depot)
        
        return {
            'transaction': depot,
            'commissions_distribuees': commissions
        }


class RetraitSerializer(serializers.Serializer):
    """Serializer pour créer un retrait."""
    montant = serializers.DecimalField(max_digits=12, decimal_places=2)
    moyen_paiement = serializers.ChoiceField(choices=Transaction.MOYEN_PAIEMENT_CHOICES)
    phone_number = serializers.CharField(max_length=15, required=True)
    
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à 0.")
        return value
    
    def create(self, validated_data):
        utilisateur = self.context['request'].user
        montant = validated_data['montant']
        
        # Calculer les frais (25%)
        frais, montant_net = CommissionService.calculer_frais_retrait(montant)
        
        # Créer la transaction de retrait
        retrait = Transaction.objects.create(
            utilisateur=utilisateur,
            type_transaction='RETRAIT',
            montant=montant,
            frais=frais,
            montant_net=montant_net,
            moyen_paiement=validated_data['moyen_paiement'],
            reference_paiement=validated_data['phone_number'],  # On stocke le numéro ici
            statut='VALIDEE',
            description=f"Retrait via {validated_data['moyen_paiement']} vers {validated_data['phone_number']} (frais: {frais} FCFA)"
        )
        
        return retrait


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