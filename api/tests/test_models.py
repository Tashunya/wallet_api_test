from django.test import TestCase
from django.db import IntegrityError
from decimal import Decimal
from ..models import Wallet, Operation


class WalletTest(TestCase):

    def setUp(self):
        Wallet.objects.create(name="Test Wallet 1", balance=5000.00)
        Wallet.objects.create(name="Test Wallet 2", balance=Decimal(-1000.00))

    def test_saved_wallets(self):
        wallets = Wallet.objects.count()
        self.assertEqual(wallets, 2)

    def test_wallet_obj_balances(self):
        wallet_obj = Wallet.objects.get(name="Test Wallet 1")
        self.assertEqual(wallet_obj.balance, Decimal(5000.00))
        wallet_obj = Wallet.objects.get(name="Test Wallet 2")
        self.assertEqual(wallet_obj.balance, Decimal(-1000.00))

    def test_duplicate_name_wallet_fail(self):
        with self.assertRaises(IntegrityError):
            Wallet.objects.create(name="Test Wallet 1", balance=Decimal(
                10000.00))
            wallets = Wallet.objects.count()
            self.assertEqual(wallets, 2)

    def test_zero_balance(self):
        Wallet.objects.create(name="Test Wallet 3", balance=0)
        wallet_obj = Wallet.objects.get(name="Test Wallet 3")
        self.assertEqual(wallet_obj.balance, Decimal(0.00))


class OperationTest(TestCase):

    def setUp(self):
        Wallet.objects.create(name="Test Wallet 1", balance=5000.00)
        Wallet.objects.create(name="Test Wallet 2", balance=Decimal(-1000.00))
        self.wallet = Wallet.objects.get(id=1)
        Operation.objects.create(type=0, wallet=self.wallet, amount=500,
                                 comment="")

    def test_saved_operations(self):
        operations = Operation.objects.count()
        self.assertEqual(operations, 1)

    def test_operation_create(self):
        wallet = Wallet.objects.get(name="Test Wallet 2")
        amount_for_change = 500
        check_balance = wallet.balance + Decimal(amount_for_change)
        Operation.objects.create(type=1, wallet=wallet,
                                 amount=amount_for_change,
                                 comment="Plus 500")
        self.assertEqual(wallet.balance, check_balance)

    def test_operations_delete(self):
        initial_balance = self.wallet.balance
        amount_for_change = 500
        operation = Operation.objects.create(type=1, wallet=self.wallet,
                                             amount=amount_for_change,
                                             comment="Plus 500")
        self.assertEqual(self.wallet.balance, initial_balance + Decimal(
            500.00))
        operation.delete()
        self.assertEqual(self.wallet.balance, initial_balance)
