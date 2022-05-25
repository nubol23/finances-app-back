from django.db import models


class TransactionType(models.TextChoices):
    INCOME = "INCOME", "income transaction"
    EXPENSE = "EXPENSE", "expense transaction"
