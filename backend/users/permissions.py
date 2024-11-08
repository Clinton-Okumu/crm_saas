from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist

class BaseModulePermission(BasePermission):
    """
    Base permission class that handles module access and role hierarchy.
    Provides a foundation for module-specific permissions with role-based access control.
    """
    # Default attributes for module-specific subclasses
    module = None
    admin_role = None
    manager_role = None
    staff_role = None
    
    # Central role hierarchy for all modules
    ROLE_HIERARCHY = {
        'super_admin': 4,  # Highest level
        'admin': 3,
        'manager': 2,
        'staff': 1         # Lowest level
    }

    def has_module_access(self, request):
        """Check if the user has access to the specified module."""
        return bool(request.user and request.user.is_authenticated and self.module in request.user.accessible_modules)

    def get_role_level(self, user):
        """Retrieve the user's level based on their role in the module hierarchy."""
        # Using constants or enums could avoid hard-coded role names
        if user.role == 'super_admin':
            return self.ROLE_HIERARCHY['super_admin']
        elif user.role == self.admin_role:
            return self.ROLE_HIERARCHY['admin']
        elif user.role == self.manager_role:
            return self.ROLE_HIERARCHY['manager']
        elif user.role == self.staff_role:
            return self.ROLE_HIERARCHY['staff']
        return 0

    def has_permission(self, request, view):
        """
        Determine if the user has general access permissions for the view based on role level.
        """
        if not self.has_module_access(request.user):
            return False

        user_level = self.get_role_level(request.user)

        # Super admin and module admin have full access
        if user_level >= self.ROLE_HIERARCHY['admin']:
            return True

        # Managers can do everything except DELETE
        if user_level >= self.ROLE_HIERARCHY['manager']:
            return request.method != 'DELETE'

        # Staff have read-only access
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has specific permissions to interact with an object.
        """
        if not self.has_module_access(request.user):
            return False

        user_level = self.get_role_level(request.user)

        # Super admin and module admin have full access
        if user_level >= self.ROLE_HIERARCHY['admin']:
            return True

        # Managers can modify but not delete
        if user_level >= self.ROLE_HIERARCHY['manager']:
            if request.method == 'DELETE':
                return False
            try:
                if hasattr(obj, 'role') and self.get_role_level(obj) >= self.ROLE_HIERARCHY['admin']:
                    return False
            except AttributeError:
                pass
            return True

        # Staff have read-only access
        if request.method in SAFE_METHODS:
            return True

        # Users can always modify their own records
        try:
            return (hasattr(obj, 'user_id') and obj.user_id == request.user.id) or \
                   (hasattr(obj, 'employee_id') and obj.employee_id == request.user.id)
        except (AttributeError, ObjectDoesNotExist):
            return False


class HRModulePermission(BaseModulePermission):
    """
    Permission class for HR module with specific role hierarchy.
    """
    module = 'hrm'
    admin_role = 'hr_admin'
    manager_role = 'hr_manager'
    staff_role = 'hr_staff'

    # Use constants or mappings for defining action-specific requirements
    ACTION_LEVELS = {
        'create_department': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'modify_department': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'view_department': BaseModulePermission.ROLE_HIERARCHY['staff'],
        
        'create_employee': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'modify_employee': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'view_employee': BaseModulePermission.ROLE_HIERARCHY['staff'],
        
        'manage_salary': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'view_salary': BaseModulePermission.ROLE_HIERARCHY['manager'],
        
        'create_leave': BaseModulePermission.ROLE_HIERARCHY['staff'],  # Everyone can create
        'approve_leave': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'view_leave': BaseModulePermission.ROLE_HIERARCHY['staff']
    }

    def get_required_level(self, action):
        """
        Define the minimum role level required for specific actions.
        Falls back to admin level if action is not defined.
        """
        return self.ACTION_LEVELS.get(action, BaseModulePermission.ROLE_HIERARCHY['admin'])

    def has_action_permission(self, request, action):
        """
        Check if user has permission for a specific action within the HR module.
        """
        user_level = self.get_role_level(request.user)
        required_level = self.get_required_level(action)
        return user_level >= required_level
