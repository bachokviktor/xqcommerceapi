from rest_framework import permissions


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    This permission class checks whether
    the user is the seller of an object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.seller


class IsReviewAuthor(permissions.BasePermission):
    """
    This permission class checks whether
    the user is the author of a review.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
