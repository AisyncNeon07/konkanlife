from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: read access for everyone, write access only for the owner.

    The model instance must have an `uploaded_by` attribute that is a Profile,
    and the request.user must have a `.profile` attribute.
    """
    message = "You can only modify content that you created."

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS — always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner of the object
        if not request.user.is_authenticated:
            return False

        try:
            return obj.uploaded_by == request.user.profile
        except AttributeError:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admins can write; everyone else can only read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
