from rest_framework import generics
from .models import Wallet, Operation
from .serializers import WalletSerializer, WalletListSerializer,\
    OperationSerializer


class WalletListView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletListSerializer


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class OperationListView(generics.ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class OperationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    http_method_names = ['delete', 'head']
