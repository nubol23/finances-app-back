from django.urls import path

from apps.transactions.views import TransactionViewSet

app_name = "transactions"
urlpatterns = [
    path("", TransactionViewSet.as_view({"get": "list"}), name="transactions-list"),
]
