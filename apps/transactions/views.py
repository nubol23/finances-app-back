from rest_framework.permissions import IsAuthenticated

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer
from utils.views import CustomModelViewSet


class TransactionViewSet(CustomModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
