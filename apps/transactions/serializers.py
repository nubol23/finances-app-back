from rest_framework.serializers import ModelSerializer

from apps.transactions.models import Transaction


class TransactionSerializer(ModelSerializer):
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
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
