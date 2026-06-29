from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transaction, DistributionCommission
from .serializers import (
    TransactionSerializer, 
    DistributionCommissionSerializer,
    DepotSerializer,
    RetraitSerializer
)


class DepotView(APIView):
    """Créer un dépôt et distribuer les commissions."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = DepotSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        return Response({
            'message': 'Dépôt effectué avec succès',
            'transaction': TransactionSerializer(result['transaction']).data,
            'commissions_distribuees': result['commissions_distribuees']
        }, status=status.HTTP_201_CREATED)


class RetraitView(APIView):
    """Créer un retrait avec calcul automatique des frais (25%)."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RetraitSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        retrait = serializer.save()
        
        return Response({
            'message': 'Retrait effectué avec succès',
            'transaction': TransactionSerializer(retrait).data
        }, status=status.HTTP_201_CREATED)


class TransactionListView(generics.ListAPIView):
    """Lister toutes les transactions de l'utilisateur connecté."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(utilisateur=self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    """Voir le détail d'une transaction."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(utilisateur=self.request.user)


class DistributionCommissionListView(generics.ListAPIView):
    """Lister les commissions reçues par l'utilisateur."""
    serializer_class = DistributionCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DistributionCommission.objects.filter(beneficiaire=self.request.user)