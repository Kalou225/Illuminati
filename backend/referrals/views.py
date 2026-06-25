from rest_framework import generics, permissions
from .models import Loge, NiveauReferral, RelationParrainage
from .serializers import LogeSerializer, NiveauReferralSerializer, RelationParrainageSerializer


class LogeListView(generics.ListCreateAPIView):
    """Lister toutes les loges ou en créer une nouvelle."""
    queryset = Loge.objects.all()
    serializer_class = LogeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LogeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Voir, modifier ou supprimer une loge spécifique."""
    queryset = Loge.objects.all()
    serializer_class = LogeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NiveauReferralListView(generics.ListAPIView):
    """Lister tous les niveaux de commission (lecture seule)."""
    queryset = NiveauReferral.objects.all()
    serializer_class = NiveauReferralSerializer
    permission_classes = [permissions.AllowAny]


class RelationParrainageListView(generics.ListCreateAPIView):
    """Lister ou créer des relations de parrainage."""
    serializer_class = RelationParrainageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Retourner les relations de l'utilisateur connecté
        user = self.request.user
        return RelationParrainage.objects.filter(
            parrain=user
        ) | RelationParrainage.objects.filter(
            filleul=user
        )