from rest_framework import permissions
from .models import Document
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a document to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

