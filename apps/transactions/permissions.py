from rest_framework import permissions


class HasTransactionAccess(permissions.BasePermission):
    message = "User does not have access to this transaction"

    def has_permission(self, request, view):
        return request.user.transactions.filter(
            id=view.kwargs.get("transaction_id")
        ).exists()
