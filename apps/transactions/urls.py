from django.urls import path

from apps.transactions.views import TransactionViewSet

app_name = "transactions"
urlpatterns = [
    path(
        "",
        TransactionViewSet.as_view({"get": "list", "post": "create"}),
        name="transactions-list",
    ),
    path("summary/", TransactionViewSet.as_view({"get": "summary"}), name="summary"),
    path(
        "<transaction_id>/",
        TransactionViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="transactions-details",
    ),
]
