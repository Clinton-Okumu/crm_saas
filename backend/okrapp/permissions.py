from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to Super Admin users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'super_admin'


class IsProjectAdmin(permissions.BasePermission):
    """
    Allows access to Project Admins and users with roles that can manage OKRs for a project.
    """
    def has_permission(self, request, view):
        return request.user.role in ['project_admin', 'project_manager']


class IsHRManager(permissions.BasePermission):
    """
    Allows access to HR Managers.
    """
    def has_permission(self, request, view):
        return request.user.role == 'hr_manager'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow owners of an objective to edit it, others can only view.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions to any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write permissions only to the owner
        return obj.owner == request.user

