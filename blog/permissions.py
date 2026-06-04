from rest_framework.permissions import BasePermission
from .models import Role


class IsAdminUserOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.ADMIN
        )

class IsCashierUserOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == Role.CASHIER
        )





