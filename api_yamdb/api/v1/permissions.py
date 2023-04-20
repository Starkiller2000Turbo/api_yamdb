from django.http import HttpRequest
from rest_framework import permissions, viewsets


class IsAdmin(permissions.BasePermission):
    """Доступно только для администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
    ) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj) -> bool:
        return True
