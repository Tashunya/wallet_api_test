from django.test import TestCase
from decimal import Decimal
from ..serializers import OperationSerializer, OperationListSerializer, \
    WalletSerializer, WalletListSerializer
from ..models import Wallet, Operation


class WalletSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {"name": "Test Wallet 1", "balance": 5000}

        self.fields = ["id", "name", "balance", "operations"]
        self.wallet = Wallet.objects.create(**self.valid_data)
        self.serializer = WalletSerializer(instance=self.wallet)

    def test_contains_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(self.fields))
        self.assertTrue(data['operations'] == [])

    def test_wallet_update(self):
        update_data = {"name": "Updated name"}
        updated_wallet = self.serializer.update(self.wallet, update_data)
        self.assertTrue(updated_wallet.name == update_data["name"])

    def test_wallet_update_balance_fail(self):
        update_data = {"name": "Updated name", "balance": 3000}
        initial_balance = self.wallet.balance
        updated_wallet = self.serializer.update(self.wallet, update_data)
        self.assertTrue(updated_wallet.name == update_data["name"])
        self.assertFalse(updated_wallet.balance == update_data["balance"])
        self.assertEqual(updated_wallet.balance, initial_balance)


class WalletListSerializerTest(TestCase):

    def setUp(self):
        self.wallet_1 = Wallet.objects.create(name="Test Wallet 1",
                                              balance=5000.00)
        self.wallet_2 = Wallet.objects.create(name="Test Wallet 2",
                                              balance=Decimal(-1000.00))
        self.valid_data = {"name": "Test Wallet 3", "balance": 5000}
        self.invalid_data = {"name": "Test Wallet 4",
                             "balance": "куку"}
        self.fields = ["id", "name", "balance"]

    def test_saved_wallets(self):
        wallets = Wallet.objects.all()
        serializer = WalletListSerializer(data=wallets, many=True)
        serializer.is_valid()
        self.assertEqual(len(serializer.data), len(wallets))

    def test_contains_fields(self):
        wallets = Wallet.objects.all()
        serializer = WalletListSerializer(data=wallets, many=True)
        serializer.is_valid()
        data = serializer.data[0]
        self.assertEqual(set(data.keys()), set(self.fields))

    def test_valid_data(self):
        serializer = WalletListSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_balance(self):
        serializer = WalletListSerializer(data=self.invalid_data)
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'balance'})


class OperationSerializerTest(TestCase):

    def setUp(self):
        self.wallet_data = {"name": "Test Wallet 1", "balance": 5000}
        self.wallet = Wallet.objects.create(**self.wallet_data)
        self.fields = ["id", "date", "type", "amount", "comment", "wallet"]
        self.operation_data = {
            "date": '2020-01-01T12:00:00',
            "type": 1,
            "amount": 2000.00,
            "wallet": self.wallet,
            "comment": "Random comment"
        }
        self.operation = Operation.objects.create(**self.operation_data)
        self.serializer = OperationSerializer(instance=self.operation)

    def test_contains_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(self.fields))


class OperationListSerializerTest(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(name="Test Wallet 1",
                                              balance=5000.00)
        operation_data_1 = {
            "date": '2020-01-01T12:00:00',
            "type": 0,
            "amount": 1000.00,
            "wallet": self.wallet,
            "comment": "Random comment 1"
        }
        operation_data_2 = {
            "date": '2020-01-01T12:00:00',
            "type": 1,
            "amount": 1000.00,
            "wallet": self.wallet,
            "comment": "Random comment 2"
        }
        Operation.objects.create(**operation_data_1)
        Operation.objects.create(**operation_data_2)

        self.operation_data = {
            "date": '2020-01-01T12:00:00',
            "type": 1,
            "amount": 2000.00,
            "comment": "Random comment"
        }
        self.invalid_data = {
            "date": '2020-01-01T12:00:00',
            "type": 3,
            "amount": 2000.00,
            "comment": "Random comment"
        }
        self.fields = ["id", "date", "type", "amount", "comment"]
        self.operations = Operation.objects.all()
        self.serializer = OperationListSerializer(data=self.operations,
                                                  many=True)

    def test_saved_operations(self):
        self.serializer.is_valid()
        self.assertEqual(len(self.serializer.data), len(self.operations))

    def test_contains_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data[0]
        self.assertEqual(set(data.keys()), set(self.fields))

    def test_valid_data(self):
        serializer = OperationListSerializer(data=self.operation_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_type(self):
        serializer = OperationListSerializer(data=self.invalid_data)
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'type'})
