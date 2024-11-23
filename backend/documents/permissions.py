from rest_framework import permissions


class IsDocumentOwnerOrShared(permissions.BasePermission):
    """
    Custom permission to allow only owners or shared users to access a document.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner or has access via sharing.
        """
        if request.method in permissions.SAFE_METHODS:
            return obj.created_by == request.user or request.user in obj.shared_with.all()
        return obj.created_by == request.user

