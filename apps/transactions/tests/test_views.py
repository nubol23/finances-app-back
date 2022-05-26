from django.urls import reverse
from rest_framework import status

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
