from rest_framework import serializers
from datetime import datetime
from .models import Wallet, Operation


class OperationSerializer(serializers.ModelSerializer):
    """ Serialize all operations """
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Operation
        fields = '__all__'


class OperationListSerializer(serializers.ModelSerializer):
    """ Serializer operations for certain wallet """
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Operation
        exclude = ('wallet', )


class WalletSerializer(serializers.ModelSerializer):
    """ Serialize certain wallet with operation list"""
    operations = OperationListSerializer(read_only=True, many=True)
    balance = serializers.DecimalField(read_only=True, max_digits=12,
                                       decimal_places=2)

    class Meta:
        model = Wallet
        fields = ("id", "name", "balance", 'operations')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class WalletListSerializer(serializers.ModelSerializer):
    """ Serialize all wallets """
    class Meta:
        model = Wallet
        exclude = ('created', )

    def create(self, validated_data):
        validated_data['created'] = datetime.now()
        new_wallet = Wallet.objects.create(**validated_data)
        return new_wallet
