from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
     Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the self user.
        if obj._meta.object_name == 'CustomUser':
            return obj.id == request.user.id

        # Write permissions are only allowed to the owner of the device.
        if hasattr(obj, 'device'):
            return obj.device.owner == request.user
        if hasattr(obj, 'track'):
            return obj.track.device.owner == request.user
        return obj.owner == request.user
