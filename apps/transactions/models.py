import uuid

from django.db import models

from apps.transactions import enums
from apps.users.models import User
from utils.models import BaseModel


class Transaction(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    title = models.CharField()
    description = models.CharField()
    value = models.FloatField()
    type = models.CharField(
        max_length=10,
        default=enums.TransactionType.EXPENSE,
        choices=enums.TransactionType.choices,
    )
    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.CASCADE
    )
