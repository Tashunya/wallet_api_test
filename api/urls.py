from django.urls import path
from api import views

urlpatterns = [
    path('wallets', views.WalletList.as_view()),
    path('wallets/<pk>', views.WalletDetail.as_view()),
    path('operations', views.OperationListView.as_view()),
    path('operations/<pk>', views.OperationView.as_view())
]
