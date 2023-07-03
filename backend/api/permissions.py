"""Describe permission classes for views in an Api app."""
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Define permission.

    Check if author is using view function or alllow read only methods.
    """

    def has_permission(self, request, view):
        """Check if user has right to request.

        If he is authenticated or request method is safe.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Check if user has right to object.

        If he is author or request method is safe.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
