from django.urls import path

from . import views

urlpatterns = [
    path('stock/', views.StockDataLiveAPIView.as_view(), name='stock-data'),
    path('crypto/', views.CryptoDataLiveAPIView.as_view(), name='crypto-data'),
]
