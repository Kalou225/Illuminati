from rest_framework import serializers
from .models import Loge, NiveauReferral, RelationParrainage
from accounts.serializers import UserSerializer

class NiveauReferralSerializer(serializers.ModelSerializer):
    """Serializer pour les niveaux de referral."""
    class Meta:
        model = NiveauReferral
        fields = ['id', 'nom', 'niveau', 'pourcentage_commission', 'description']


class LogeSerializer(serializers.ModelSerializer):
    """Serializer pour les loges."""
    grand_maitre_details = UserSerializer(source='grand_maitre', read_only=True)
    
    class Meta:
        model = Loge
        fields = ['id', 'nom', 'description', 'grand_maitre', 'grand_maitre_details', 'date_creation', 'est_active']
        read_only_fields = ['id', 'date_creation']


class RelationParrainageSerializer(serializers.ModelSerializer):
    """Serializer pour les relations de parrainage."""
    parrain_details = UserSerializer(source='parrain', read_only=True)
    filleul_details = UserSerializer(source='filleul', read_only=True)
    niveau_details = NiveauReferralSerializer(source='niveau', read_only=True)
    
    class Meta:
        model = RelationParrainage
        fields = [
            'id', 'parrain', 'parrain_details', 
            'filleul', 'filleul_details',
            'niveau', 'niveau_details',
            'date_parrainage', 'est_actif'
        ]
        read_only_fields = ['id', 'date_parrainage']