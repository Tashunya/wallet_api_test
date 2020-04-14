from rest_framework import serializers
from datetime import datetime
from .models import Wallet, Operation


class OperationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Operation
        fields = '__all__'

    def create(self, validated_data):
        new_operation = Operation.objects.create(**validated_data)
        return new_operation


class OperationListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Operation
        exclude = ('wallet', )


class WalletSerializer(serializers.ModelSerializer):
    operations = OperationListSerializer(read_only=True, many=True)

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


class WalletListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        exclude = ('created', )
