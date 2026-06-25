from django.urls import path
from .views import (
    TransactionListView, TransactionDetailView,
    DistributionCommissionListView
)

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transactions-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('commissions/', DistributionCommissionListView.as_view(), name='commissions-list'),
]