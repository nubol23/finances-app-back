from django.urls import path

from apps.transactions.views import TransactionViewSet

app_name = "transactions"
urlpatterns = [
    path(
        "",
        TransactionViewSet.as_view({"get": "list", "post": "create"}),
        name="transactions-list",
    ),
    path(
        "/<transaction_id>/",
        TransactionViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
        name="transactions-details",
    ),
]
