from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    """
    Allows access only to super admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'super_admin')

class IsHRAdmin(BasePermission):
    """
    Allows access only to HR admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'hr_admin')

class CanManageUsers(BasePermission):
    """
    Permission to manage users based on role hierarchy
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Super admin can do anything
        if request.user.role == 'super_admin':
            return True

        # HR admin can manage most users except super admin
        if request.user.role == 'hr_admin':
            return True

        # Read-only for safe methods if user has HR module access
        if request.method in SAFE_METHODS:
            return 'hrm' in request.user.accessible_modules

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Super admin can do anything
        if request.user.role == 'super_admin':
            return True

        # HR admin can't modify super admin
        if request.user.role == 'hr_admin' and obj.role != 'super_admin':
            return True

        # Users can view/edit their own profile
        if request.method in SAFE_METHODS and obj == request.user:
            return True

        return False