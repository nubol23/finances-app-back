from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.transactions.enums import TransactionType
from apps.transactions.models import Transaction
from apps.transactions.permissions import HasTransactionAccess
from apps.transactions.serializers import TransactionSerializer
from utils.views import CustomModelViewSet


class TransactionViewSet(CustomModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "transaction_id"

    def get_permissions(self):
        if self.action in ["retrieve", "partial_update", "delete"]:
            self.permission_classes = self.permission_classes + [HasTransactionAccess]

        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)

        month_year = self.request.query_params.get("month_year")
        if month_year:
            month, year = month_year.split("-")
            qs = qs.filter(date__month=month, date__year=year)

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, *args, **kwargs):
        qs = self.get_queryset()

        income = qs.filter(type=TransactionType.INCOME).aggregate(value=Sum("value"))[
            "value"
        ]
        expense = qs.filter(type=TransactionType.EXPENSE).aggregate(value=Sum("value"))[
            "value"
        ]
        data = {"income": income, "expense": expense, "total": income - expense}

        return Response(data, status=status.HTTP_200_OK)
