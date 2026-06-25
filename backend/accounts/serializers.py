from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les informations utilisateur."""
    sponsor_name = serializers.CharField(source='sponsor.full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone_number', 'full_name', 'grade',
            'sponsor', 'sponsor_name', 'referral_code',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'email', 'phone_number', 'full_name', 'password', 
            'password_confirm', 'sponsor', 'referral_code'
        ]
    
    def validate(self, data):
        # Vérifier que les mots de passe correspondent
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data
    
    def create(self, validated_data):
        # Retirer password_confirm car ce n'est pas un champ du modèle
        validated_data.pop('password_confirm')
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            sponsor=validated_data.get('sponsor'),
            referral_code=validated_data.get('referral_code')
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer pour la connexion."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)