from django.urls import path
from .views import (
    LogeListView, LogeDetailView,
    NiveauReferralListView,
    RelationParrainageListView
)

urlpatterns = [
    path('loges/', LogeListView.as_view(), name='loges-list'),
    path('loges/<int:pk>/', LogeDetailView.as_view(), name='loge-detail'),
    path('niveaux/', NiveauReferralListView.as_view(), name='niveaux-list'),
    path('parrainages/', RelationParrainageListView.as_view(), name='parrainages-list'),
]