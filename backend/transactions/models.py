from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Transaction(models.Model):
    """Enregistre toutes les transactions financières."""
    
    TYPE_CHOICES = [
        ('DEPOT', 'Dépôt'),
        ('RETRAIT', 'Retrait'),
        ('COMMISSION', 'Commission'),
        ('BONUS', 'Bonus'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    MOYEN_PAIEMENT_CHOICES = [
        ('WAVE', 'Wave CI'),
        ('MOOV', 'Moov Money'),
        ('MTN', 'MTN Mobile Money'),
        ('ORANGE', 'Orange Money'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Utilisateur"
    )
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant (FCFA)")
    frais = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name="Frais (FCFA)"
    )
    montant_net = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant net (FCFA)"
    )
    moyen_paiement = models.CharField(
        max_length=20, 
        choices=MOYEN_PAIEMENT_CHOICES,
        blank=True,
        null=True,
        verbose_name="Moyen de paiement"
    )
    reference_paiement = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Référence paiement externe"
    )
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='EN_ATTENTE',
        verbose_name="Statut"
    )
    date_transaction = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    # Pour les commissions : lien vers la transaction originale
    transaction_originale = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='commissions',
        verbose_name="Transaction originale"
    )
    niveau_commission = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name="Niveau de commission"
    )

    class Meta:
        ordering = ['-date_transaction']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.type_transaction} - {self.utilisateur.full_name} - {self.montant} FCFA"

    def save(self, *args, **kwargs):
        # Calcul automatique du montant net
        if self.type_transaction == 'RETRAIT':
            # 25% de frais de retrait
            self.frais = self.montant * Decimal('0.25')
            self.montant_net = self.montant - self.frais
        else:
            self.montant_net = self.montant
        super().save(*args, **kwargs)


class DistributionCommission(models.Model):
    """Trace la distribution des commissions selon la hiérarchie."""
    
    transaction_source = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='distributions',
        verbose_name="Transaction source"
    )
    beneficiaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commissions_recues',
        verbose_name="Bénéficiaire"
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant (FCFA)")
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage (%)")
    niveau = models.IntegerField(verbose_name="Niveau de distribution")
    date_distribution = models.DateTimeField(auto_now_add=True)
    est_paye = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Distribution de commission"
        verbose_name_plural = "Distributions de commission"

    def __str__(self):
        return f"{self.beneficiaire.full_name} - {self.montant} FCFA (Niveau {self.niveau})"