from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # API Authentication (JWT)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API de notre application
    path('api/accounts/', include('accounts.urls')),
    path('api/referrals/', include('referrals.urls')),
    path('api/transactions/', include('transactions.urls')),
]