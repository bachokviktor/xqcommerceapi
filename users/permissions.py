from rest_framework import permissions


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    """
    This custom permission class checks whether
    selected user is the current user, otherwise
    read-only permission is granted.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
