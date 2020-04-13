from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Wallet, Operation


class OperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = ('id', 'date', 'type', 'amount', 'wallet', 'comment')

    def create(self, validated_data):
        new_operation = Operation.objects.create(**validated_data)
        return new_operation


class WalletSerializer(serializers.ModelSerializer):
    operations = OperationSerializer(read_only=True, many=True)

    class Meta:
        model = Wallet
        fields = ("id", "name", "balance", 'operations')

    def create(self, validated_data):
        validated_data['created'] = datetime.now()
        new_wallet = Wallet.objects.create(**validated_data)
        return new_wallet

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
