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


class IsAuthorOrModeratorOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly,
):
    """Права доступа для отзывов и коментариев."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
