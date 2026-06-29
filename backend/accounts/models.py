from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """Gestionnaire pour créer des utilisateurs et super-utilisateurs."""
    
    def create_user(self, email, phone_number, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        if not phone_number:
            raise ValueError('Le numéro de téléphone est obligatoire')
            
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('grade', 'GRAND_MAITRE') # Le superuser est le Grand Maître par défaut
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, phone_number, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé pour Illuminati."""
    
    GRADE_CHOICES = [
        ('APPRENTI', 'Apprenti'),
        ('COMPAGNON', 'Compagnon'),
        ('MAITRE', 'Maître'),
        ('GRAND_MAITRE', 'Grand Maître'),
    ]

    # Informations de base
    email = models.EmailField(unique=True, verbose_name="Adresse Email")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Numéro de téléphone")
    full_name = models.CharField(max_length=100, verbose_name="Nom complet")
    
    # Grade dans la loge
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='APPRENTI', verbose_name="Grade")
    
    # Droits et statut
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Système de parrainage
    sponsor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sponsored_users',
        verbose_name="Parrain"
    )
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Code de parrainage")

    objects = UserManager()

    # On utilise l'email pour se connecter au lieu du username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'full_name']
    def save(self, *args, **kwargs):
        # Générer un code de parrainage unique si l'utilisateur n'en a pas
        if not self.referral_code:
            import uuid
            # Crée un code court basé sur le nom et un identifiant unique
            short_uuid = uuid.uuid4().hex[:4].upper()
            name_prefix = self.full_name.split()[0][:3].upper() if self.full_name else 'USR'
            self.referral_code = f"{name_prefix}-{short_uuid}"
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.full_name} ({self.grade})"