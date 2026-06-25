from django.db import models
from django.conf import settings
from django.utils import timezone

class Loge(models.Model):
    """Représente une loge maçonnique (niveau de regroupement)."""
    
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la loge")
    description = models.TextField(blank=True, verbose_name="Description")
    grand_maitre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loges_dirigees',
        verbose_name="Grand Maître"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Loge"
        verbose_name_plural = "Loges"

    def __str__(self):
        return f"Loge {self.nom} - GM: {self.grand_maitre.full_name}"


class NiveauReferral(models.Model):
    """Niveaux de la hiérarchie de parrainage."""
    
    nom = models.CharField(max_length=50, unique=True, verbose_name="Nom du niveau")
    niveau = models.IntegerField(unique=True, verbose_name="Ordre du niveau")
    pourcentage_commission = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Pourcentage de commission (%)"
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['niveau']
        verbose_name = "Niveau de referral"
        verbose_name_plural = "Niveaux de referral"

    def __str__(self):
        return f"Niveau {self.niveau}: {self.nom} ({self.pourcentage_commission}%)"


class RelationParrainage(models.Model):
    """Enregistre les relations de parrainage entre utilisateurs."""
    
    parrain = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parrainages_donnes',
        verbose_name="Parrain"
    )
    filleul = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parrainages_recus',
        verbose_name="Filleul"
    )
    date_parrainage = models.DateTimeField(auto_now_add=True)
    niveau = models.ForeignKey(
        NiveauReferral,
        on_delete=models.CASCADE,
        verbose_name="Niveau de relation"
    )
    est_actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ['parrain', 'filleul']
        verbose_name = "Relation de parrainage"
        verbose_name_plural = "Relations de parrainage"

    def __str__(self):
        return f"{self.parrain.full_name} → {self.filleul.full_name} (Niveau {self.niveau.niveau})"