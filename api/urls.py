from django.urls import path
from api import views

urlpatterns = [
    path('wallets', views.WalletListView.as_view(),
         name="wallet_list"),
    path('wallets/<pk>', views.WalletDetailView.as_view(),
         name="wallet"),
    path('operations', views.OperationListView.as_view(),
         name="operation_list"),
    path('operations/<pk>', views.OperationDetailView.as_view(),
         name="operation")
]
