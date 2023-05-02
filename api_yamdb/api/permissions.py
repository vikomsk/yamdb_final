from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == ADMIN:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True


class IsUserOrAdminOrModerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user or request.user.role in (
                ADMIN,
                MODERATOR,
            )
        return request.method in permissions.SAFE_METHODS
