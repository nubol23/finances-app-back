from datetime import datetime, timedelta, timezone

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from apps.transactions.enums import TransactionType
from apps.transactions.models import Transaction
from apps.transactions.tests.factories import TransactionFactory
from apps.transactions.tests.validators import ValidateTransaction
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class TransactionListViewSetTests(CustomTestCase):

    FREEZE_TIME = "2022-01-01T00:00:00Z"

    @classmethod
    @freeze_time(FREEZE_TIME)
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

        # self.transactions.reverse()
        ValidateMultiple.validate(
            self,
            ValidateTransaction.validate,
            self.transactions,
            response.json(),
        )

    @freeze_time(FREEZE_TIME)
    def test_list_user_by_month_year(self):
        self.transactions[1].date += timedelta(days=32)
        self.transactions[1].save()
        self.transactions[2].date += timedelta(days=397)
        self.transactions[2].save()

        response = self.backend.get(
            self.url, data={"month_year": "01-2022"}, status=status.HTTP_200_OK
        )
        ValidateMultiple.validate(
            self,
            ValidateTransaction.validate,
            [self.transactions[0]],
            response.json(),
        )

        response = self.backend.get(
            self.url, data={"month_year": "02-2022"}, status=status.HTTP_200_OK
        )
        ValidateMultiple.validate(
            self,
            ValidateTransaction.validate,
            [self.transactions[1]],
            response.json(),
        )

        response = self.backend.get(
            self.url, data={"month_year": "02-2023"}, status=status.HTTP_200_OK
        )
        ValidateMultiple.validate(
            self,
            ValidateTransaction.validate,
            [self.transactions[2]],
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
        count = Transaction.objects.count()

        response = self.backend.post(
            self.url, self.data, status=status.HTTP_201_CREATED
        )

        transaction = Transaction.objects.latest("created_on")
        ValidateTransaction.validate(self, transaction, response.json())
        self.assertEqual(Transaction.objects.count(), count + 1)


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

    def test_retrieve_transaction_without_access_fail(self):
        another_transaction = TransactionFactory()

        url = reverse(
            "transactions:transactions-details",
            kwargs={"transaction_id": another_transaction.id},
        )
        response = self.backend.get(url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User does not have access to this transaction"
        )


class TransactionUpdateViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.transaction = TransactionFactory(user=cls.user)

        cls.url = reverse(
            "transactions:transactions-details",
            kwargs={"transaction_id": cls.transaction.id},
        )

        cls.data = {
            "date": datetime.now(tz=timezone.utc),
            "title": "Transaction 1",
            "description": "A transaction",
            "value": 12.3,
            "type": TransactionType.INCOME,
        }

    def setUp(self):
        self.backend.login(self.user)

    def test_update_transaction(self):
        response = self.backend.patch(self.url, self.data, status=status.HTTP_200_OK)

        self.transaction.refresh_from_db()
        ValidateTransaction.validate(self, self.transaction, response.json())

    def test_update_transaction_without_access_fail(self):
        another_transaction = TransactionFactory()

        url = reverse(
            "transactions:transactions-details",
            kwargs={"transaction_id": another_transaction.id},
        )
        response = self.backend.patch(url, self.data, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User does not have access to this transaction"
        )


class TransactionDeleteViewSetTests(CustomTestCase):
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

    def test_update_transaction(self):
        count = Transaction.objects.count()

        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())
        self.assertEqual(Transaction.objects.count(), count - 1)


class TransactionSummaryViewSetTests(CustomTestCase):
    FREEZE_TIME = "2022-01-01T00:00:00Z"

    @classmethod
    @freeze_time(FREEZE_TIME)
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.expense_transactions = TransactionFactory.create_batch(
            size=3, user=cls.user
        )
        cls.income_transactions = TransactionFactory.create_batch(
            size=3, user=cls.user, type=TransactionType.INCOME
        )

        cls.url = reverse("transactions:summary")

    def setUp(self):
        self.backend.login(self.user)

    def _transaction_sum(self, transaction_list):
        res = 0
        for transaction in transaction_list:
            res += transaction.value

        return res

    def test_transaction_summary(self):
        response = self.backend.get(
            self.url, data={"month_year": "01-2022"}, status=status.HTTP_200_OK
        )
        response_json = response.json()

        expense = self._transaction_sum(self.expense_transactions)
        income = self._transaction_sum(self.income_transactions)
        self.assertEqual(response_json["income"], income)
        self.assertEqual(response_json["expense"], expense)
        self.assertEqual(response_json["total"], income - expense)
