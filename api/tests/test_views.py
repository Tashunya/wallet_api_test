import json
from decimal import Decimal, getcontext
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Wallet, Operation


client = Client()
getcontext().prec = 2


class WalletDetailViewTest(TestCase):

    def setUp(self):
        Wallet.objects.create(name="Test Wallet 1", balance=5000.00)
        Wallet.objects.create(name="Test Wallet 2",
                              balance=Decimal(-1000.00))

    def test_get_wallet_by_id(self):
        correct_response = {'id': 1,
                            'name': "Test Wallet 1",
                            'balance': '5000.00',
                            'operations': []}
        wallet_obj = Wallet.objects.get(name="Test Wallet 1")
        response = client.get(reverse('wallet', kwargs={'pk': wallet_obj.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, correct_response)
        self.assertEqual(len(response.data), 4)

    def test_get_wallet_by_invalid_id(self):
        invalid_pk = 100000
        response = client.get(reverse('wallet', kwargs={'pk': invalid_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wallet_by_id(self):
        wallet_obj = Wallet.objects.get(name="Test Wallet 2")
        update_payload = {'name': 'Updated Wallet'}
        response = client.put(reverse('wallet', kwargs={'pk': wallet_obj.id}),
                              data=json.dumps(update_payload),
                              content_type='application/json')
        wallet_obj.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(wallet_obj.name, update_payload["name"])

    def test_delete_wallet(self):
        wallet_obj = Wallet.objects.get(name="Test Wallet 1")
        Operation.objects.create(type=0, wallet=wallet_obj, amount=500,
                                 comment="")
        response = client.delete(reverse('wallet', kwargs={'pk':
                                                               wallet_obj.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        operations_count = Operation.objects.count()
        self.assertEqual(operations_count, 0)


class WalletListViewTest(TestCase):

    def setUp(self):
        Wallet.objects.create(name="Test Wallet 1", balance=5000.00)
        Wallet.objects.create(name="Test Wallet 2",
                              balance=Decimal(-1000.00))
        self.wallet_payload = {"name": "New Wallet",
                               "balance": 1000}

    def test_get_wallet_list(self):
        response = client.get(reverse('wallet_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_valid_wallet(self):
        response = client.post(reverse('wallet_list'),
                               data=json.dumps(self.wallet_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wallets_count = Wallet.objects.count()
        self.assertEqual(wallets_count, 3)

    def test_create_invalid_wallet_balance(self):
        invalid_payload = {"name": "Invalid Wallet",
                           "balance": "balance"}
        response = client.post(reverse('wallet_list'),
                               data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OperationDetailViewTest(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(name="Test Wallet 1",
                                          balance=5000.00)
        self.operation_payload = {"date": "2020-04-12T12:00:00",
                                  "type": 1,
                                  "amount": 0.01,
                                  "wallet": self.wallet,
                                  "comment": "Non-empty comment"
                                  }

    def test_delete_operation(self):
        operation = Operation.objects.create(**self.operation_payload)
        response = client.delete(reverse('operation',
                                         kwargs={'pk': operation.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        operations_count = Operation.objects.count()
        self.assertEqual(operations_count, 0)

    def test_get_operation_not_allowed(self):
        operation = Operation.objects.create(**self.operation_payload)
        response = client.get(reverse('operation',
                                      kwargs={'pk': operation.id}))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_operation_not_allowed(self):
        operation = Operation.objects.create(**self.operation_payload)
        response = client.put(reverse('operation',
                                      kwargs={'pk': operation.id}),
                              data={"amount": 200},
                              content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class OperationListViewTest(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(name="Test Wallet 1",
                                            balance=5000.00)
        Operation.objects.create(**{"date": "2020-01-01T12:00:00",
                                    "type": 0,
                                    "amount": 12,
                                    "wallet": self.wallet,
                                    "comment": "Non-empty comment"
                                    })

        self.wallet.refresh_from_db()
        self.operation_payload = {"date": "2020-04-12T12:00:00",
                                  "type": 1,
                                  "amount": 0.01,
                                  "wallet": self.wallet.id,
                                  "comment": "Non-empty comment"
                                  }

    def test_create_new_operation(self):
        initial_balance = self.wallet.balance
        type = self.operation_payload["type"]
        amount = [-self.operation_payload['amount'],
                  self.operation_payload['amount']][type]
        check_balance = initial_balance + Decimal(amount)

        response = client.post(reverse('operation_list'),
                               data=json.dumps(self.operation_payload),
                               content_type='application/json')

        self.wallet.refresh_from_db()
        operation_count = Operation.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(operation_count, 2)
        self.assertEqual(self.wallet.balance, check_balance)

    def test_create_invalid_operation_type(self):
        invalid_payload = {"date": "2020-04-12T12:00:00",
                                  "type": 3,
                                  "amount": 1000.00,
                                  "wallet": self.wallet.id,
                                  "comment": "Non-empty comment"
                                  }
        initial_balance = self.wallet.balance
        type = self.operation_payload["type"]
        amount = [-self.operation_payload['amount'],
                  self.operation_payload['amount']][type]
        response = client.post(reverse('operation_list'),
                               data=json.dumps(invalid_payload),
                               content_type='application/json')

        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        operation_count = Operation.objects.count()
        self.assertEqual(operation_count, 1)
        self.assertEqual(self.wallet.balance, initial_balance)

    def test_get_operation_list(self):
        response = client.get(reverse('operation_list'))
        operation_count = Operation.objects.count()
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(operation_count, len(response_body))
