from rest_framework.serializers import ModelSerializer

from apps.transactions.models import Transaction
from apps.users.serializers import UserSerializer


class TransactionSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "date",
            "title",
            "description",
            "value",
            "type",
        )
        read_only_fields = (
            "id",
            "user",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
