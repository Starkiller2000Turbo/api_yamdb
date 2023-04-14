from django.http import HttpRequest
from rest_framework import permissions, viewsets


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
    ) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )