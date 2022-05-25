from datetime import datetime, timezone

import factory.django

from apps.transactions.models import Transaction
from apps.users.tests.factories import UserFactory
from utils.tests.faker import faker


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    date = factory.LazyFunction(lambda: datetime.now(tz=timezone.utc))
    title = factory.Sequence(lambda n: f"Transaction {n}")
    value = factory.LazyFunction(lambda: faker.pyfloat(positive=True))
    user = factory.SubFactory(UserFactory)
