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
        read_only_fields = ['id', 'date_joined', 'referral_code']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'phone_number', 'full_name', 'password', 
            'password_confirm', 'referral_code'
        ]
    
    def validate(self, data):
        # Vérifier que les mots de passe correspondent
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        
        # Vérifier que le code de parrainage existe (si fourni)
        referral_code = data.get('referral_code', '').strip()
        if referral_code:
            try:
                data['sponsor'] = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                raise serializers.ValidationError({"referral_code": "Ce code de parrainage n'existe pas."})
        else:
            data['sponsor'] = None
        
        return data
    
    def create(self, validated_data):
        # Retirer les champs qui ne sont pas dans le modèle
        validated_data.pop('password_confirm')
        sponsor = validated_data.pop('sponsor', None)
        validated_data.pop('referral_code', None)  # IMPORTANT : Ne pas assigner le code du parrain !
        
        # Créer l'utilisateur (le code sera généré automatiquement par save())
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            sponsor=sponsor,
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer pour la connexion."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)