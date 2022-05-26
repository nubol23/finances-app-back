from datetime import datetime, timezone

from django.urls import reverse
from rest_framework import status

from apps.transactions.enums import TransactionType
from apps.transactions.models import Transaction
from apps.transactions.tests.factories import TransactionFactory
from apps.transactions.tests.validators import ValidateTransaction
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class TransactionListViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.transactions = TransactionFactory.create_batch(size=3, user=cls.user)
        # Expected to not be returned
        cls.other_transactions = TransactionFactory.create_batch(size=3)

        cls.url = reverse("transactions:transactions-list")

    def setUp(self):
        self.backend.login(self.user)

    def test_list_user_all_transactions(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.transactions.reverse()
        ValidateMultiple.validate(
            self,
            ValidateTransaction.validate,
            self.transactions,
            response.json(),
        )


class TransactionCreateViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.url = reverse("transactions:transactions-list")

        cls.data = {
            "date": datetime.now(tz=timezone.utc),
            "title": "Transaction 1",
            "description": "A transaction",
            "value": 12.3,
            "type": TransactionType.INCOME,
        }

    def setUp(self):
        self.backend.login(self.user)

    def test_create_transaction(self):
        response = self.backend.post(
            self.url, self.data, status=status.HTTP_201_CREATED
        )

        transaction = Transaction.objects.latest("created_on")
        ValidateTransaction.validate(self, transaction, response.json())


class TransactionRetrieveViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.transaction = TransactionFactory(user=cls.user)

        cls.url = reverse(
            "transactions:transactions-details",
            kwargs={"transaction_id": cls.transaction.id},
        )

    def setUp(self):
        self.backend.login(self.user)

    def test_retrieve_transaction(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        ValidateTransaction.validate(self, self.transaction, response.json())

    def test_retrieve_transaction_without_access(self):
        another_transaction = TransactionFactory()

        url = reverse(
            "transactions:transactions-details",
            kwargs={"transaction_id": another_transaction.id},
        )
        response = self.backend.get(url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User does not have access to this transaction"
        )
