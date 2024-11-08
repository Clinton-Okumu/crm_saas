from rest_framework.permissions import SAFE_METHODS
from users.permissions import HRModulePermission

class CanManageDepartments(HRModulePermission):
    """
    Permission class for managing departments within the HR module.
    """
    module = 'hrm'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        
        # SAFE_METHODS: Read-only access for staff, managers, and admin
        if request.method in SAFE_METHODS:
            return request.user.role in ['hr_admin', 'hr_manager', 'hr_staff']
        
        # Write access restricted to admin
        return request.user.role == 'hr_admin'

class CanManageEmployees(HRModulePermission):
    """
    Permission class for managing employees within the HR module.
    """
    module = 'hrm'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        
        # Read-only access for all; edit access for HR admin and manager
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ['hr_admin', 'hr_manager']

    def has_object_permission(self, request, view, obj):
        user = request.user

        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # HR Manager can manage employees except HR admin
        if user.role == 'hr_manager':
            return obj.role not in ['hr_admin']
        
        # HR Staff has limited access
        if user.role == 'hr_staff':
            return obj.role not in ['hr_admin', 'hr_manager']
        
        # Users can manage their own profile
        return obj.id == user.id

class CanManageSalaries(HRModulePermission):
    """
    Permission class for managing salaries within the HR module.
    """
    module = 'hrm'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # SAFE_METHODS: Read-only access for HR admin and manager
        if request.method in SAFE_METHODS:
            return request.user.role in ['hr_admin', 'hr_manager']
        
        # Only HR admin can edit salaries
        return request.user.role == 'hr_admin'

    def has_object_permission(self, request, view, obj):
        user = request.user

        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # HR Manager can manage salaries in their departments
        if user.role == 'hr_manager' and hasattr(user, 'managed_departments'):
            return obj.employee.department in user.managed_departments

        # No other roles have access to manage salaries
        return False

class CanManageLeaves(HRModulePermission):
    """
    Permission class for managing leaves within the HR module.
    """
    module = 'hrm'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # Allow all users to view, create, or read leaves
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            return True
        
        # Only HR admin and manager can edit or approve leaves
        return request.user.role in ['hr_admin', 'hr_manager']

    def has_object_permission(self, request, view, obj):
        user = request.user

        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # HR Manager can manage leaves within their departments
        if user.role == 'hr_manager' and hasattr(user, 'managed_departments'):
            return obj.employee.department in user.managed_departments

        # HR Staff can only view leaves
        if user.role == 'hr_staff':
            return request.method in SAFE_METHODS

        # Employees can view their own leaves
        return obj.employee.id == user.id
