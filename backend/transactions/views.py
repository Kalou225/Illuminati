from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Transaction, DistributionCommission
from .serializers import TransactionSerializer, DistributionCommissionSerializer


class TransactionListView(generics.ListCreateAPIView):
    """Lister ou créer des transactions."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Retourner les transactions de l'utilisateur connecté
        return Transaction.objects.filter(
            utilisateur=self.request.user
        )
    
    def perform_create(self, serializer):
        # Associer automatiquement l'utilisateur connecté
        serializer.save(utilisateur=self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    """Voir le détail d'une transaction."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(
            utilisateur=self.request.user
        )


class DistributionCommissionListView(generics.ListAPIView):
    """Lister les commissions reçues par l'utilisateur."""
    serializer_class = DistributionCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DistributionCommission.objects.filter(
            beneficiaire=self.request.user
        )