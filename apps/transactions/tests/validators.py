from apps.transactions.models import Transaction
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import BaseValidator, ValidateDateTime


class ValidateTransaction(BaseValidator):
    @staticmethod
    def _perform_validation(
        testcase: CustomTestCase, obj: Transaction, transaction_dict: dict
    ):
        testcase.assertEqual(str(obj.id), transaction_dict.pop("id"))
        ValidateDateTime.validate(testcase, obj.date, transaction_dict.pop("date"))
        testcase.assertEqual(obj.title, transaction_dict.pop("title"))
        testcase.assertEqual(obj.description, transaction_dict.pop("description"))
        testcase.assertEqual(obj.value, transaction_dict.pop("value"))
        testcase.assertEqual(obj.type, transaction_dict.pop("type"))
