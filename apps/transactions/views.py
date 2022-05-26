from rest_framework.permissions import IsAuthenticated

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
        return qs
