from django.urls import path
from .views import (
    DepotView,
    RetraitView,
    TransactionListView,
    TransactionDetailView,
    DistributionCommissionListView
)

urlpatterns = [
    path('depot/', DepotView.as_view(), name='depot'),
    path('retrait/', RetraitView.as_view(), name='retrait'),
    path('transactions/', TransactionListView.as_view(), name='transactions-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('commissions/', DistributionCommissionListView.as_view(), name='commissions-list'),
]