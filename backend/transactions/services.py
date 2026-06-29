from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Transaction, DistributionCommission
from referrals.models import NiveauReferral
from accounts.models import User

class CommissionService:
    """Service pour calculer et distribuer les commissions."""
    
    @staticmethod
    @transaction.atomic
    def distribuer_commissions(depot_transaction):
        """
        Calcule et distribue les commissions pour un dépôt.
        
        Règles :
        - Niveau 1 (Parrain direct) : 3%
        - Niveau 2 : 7%
        - Niveau 3 : 7%
        - Grand Maître : 15%
        """
        utilisateur = depot_transaction.utilisateur
        montant = depot_transaction.montant
        commissions_distribuees = []
        
        # Récupérer tous les niveaux de commission
        niveaux = NiveauReferral.objects.all().order_by('niveau')
        
        # Parcourir la chaîne de parrainage
        utilisateur_actuel = utilisateur
        niveau_courant = 1
        
        for niveau in niveaux:
            if not utilisateur_actuel or not utilisateur_actuel.sponsor:
                break
            
            parrain = utilisateur_actuel.sponsor
            pourcentage = niveau.pourcentage_commission
            montant_commission = (montant * pourcentage) / Decimal('100')
            
            # Créer la transaction de commission
            commission_transaction = Transaction.objects.create(
                utilisateur=parrain,
                type_transaction='COMMISSION',
                montant=montant_commission,
                frais=Decimal('0.00'),
                montant_net=montant_commission,
                statut='VALIDEE',
                transaction_originale=depot_transaction,
                niveau_commission=niveau_courant,
                description=f"Commission niveau {niveau_courant} sur dépôt de {utilisateur.full_name}"
            )
            
            # Créer la distribution
            distribution = DistributionCommission.objects.create(
                transaction_source=depot_transaction,
                beneficiaire=parrain,
                montant=montant_commission,
                pourcentage=pourcentage,
                niveau=niveau_courant,
                est_paye=True
            )
            
            commissions_distribuees.append({
                'beneficiaire': parrain.full_name,
                'montant': montant_commission,
                'pourcentage': pourcentage,
                'niveau': niveau_courant
            })
            
            # Passer au niveau suivant
            utilisateur_actuel = parrain
            niveau_courant += 1
        
        return commissions_distribuees
    
    @staticmethod
    def calculer_frais_retrait(montant):
        """
        Calcule les frais de retrait (25%).
        
        Retourne :
        - frais : montant des frais
        - montant_net : montant après frais
        """
        frais = (montant * Decimal('25')) / Decimal('100')
        montant_net = montant - frais
        return frais, montant_net