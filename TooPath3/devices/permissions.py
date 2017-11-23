from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
     Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'device'):
            return obj.device.owner == request.user

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
