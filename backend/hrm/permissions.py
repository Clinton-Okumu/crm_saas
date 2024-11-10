from typing import Any, ClassVar, Dict
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from users.permissions import HRModulePermission, BaseModulePermission

class CanManageDepartments(HRModulePermission):
    """
    Permission class for managing departments within the HR module.
    """
    module: str = 'hrm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_department': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_department': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'update_department': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_department': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_department',
            'POST': 'create_department',
            'PUT': 'update_department',
            'PATCH': 'update_department',
            'DELETE': 'delete_department'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_department'))


class CanManageEmployees(HRModulePermission):
    """
    Permission class for managing employees within the HR module.
    """
    module: str = 'hrm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_employee': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_employee': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'update_employee': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'delete_employee': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'manage_own_profile': BaseModulePermission.ROLE_HIERARCHY['staff'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_employee',
            'POST': 'create_employee',
            'PUT': 'update_employee',
            'PATCH': 'update_employee',
            'DELETE': 'delete_employee'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_employee'))

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user
        
        # Users can manage their own profile
        if obj.id == user.id:
            return self.has_action_permission(request, 'manage_own_profile')
        
        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # HR Manager can manage employees except HR admin
        if user.role == 'hr_manager':
            if hasattr(obj, 'role') and obj.role == 'hr_admin':
                return False
            return self.has_action_permission(request, 'update_employee')
        
        # HR Staff has view-only access to non-admin/manager employees
        if user.role == 'hr_staff':
            if hasattr(obj, 'role') and obj.role in ['hr_admin', 'hr_manager']:
                return False
            return request.method in SAFE_METHODS
            
        return False


class CanManageSalaries(HRModulePermission):
    """
    Permission class for managing salaries within the HR module.
    """
    module: str = 'hrm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_salary': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'create_salary': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'update_salary': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_salary': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'manage_department_salary': BaseModulePermission.ROLE_HIERARCHY['manager'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_salary',
            'POST': 'create_salary',
            'PUT': 'update_salary',
            'PATCH': 'update_salary',
            'DELETE': 'delete_salary'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_salary'))

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user

        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # HR Manager can view salaries in their departments
        if (user.role == 'hr_manager' and 
            hasattr(user, 'managed_departments') and 
            obj.employee.department in user.managed_departments):
            return self.has_action_permission(request, 'manage_department_salary')

        return False


class CanManageLeaves(HRModulePermission):
    """
    Permission class for managing leaves within the HR module.
    """
    module: str = 'hrm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_leave': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_leave': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'update_leave': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'delete_leave': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'approve_leave': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'manage_department_leave': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'view_own_leave': BaseModulePermission.ROLE_HIERARCHY['staff'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False

        # Everyone can create and view leaves
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return self.has_action_permission(request, 'view_leave')
        elif request.method == 'POST':
            return self.has_action_permission(request, 'create_leave')
        
        # Other actions require higher permissions
        action_mapping = {
            'PUT': 'update_leave',
            'PATCH': 'approve_leave',
            'DELETE': 'delete_leave'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_leave'))

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user

        # HR Admin has full access
        if user.role == 'hr_admin':
            return True
        
        # Users can view their own leaves
        if obj.employee.id == user.id:
            return self.has_action_permission(request, 'view_own_leave')
        
        # HR Manager can manage leaves within their departments
        if (user.role == 'hr_manager' and 
            hasattr(user, 'managed_departments') and 
            obj.employee.department in user.managed_departments):
            return self.has_action_permission(request, 'manage_department_leave')

        # HR Staff can only view leaves
        if user.role == 'hr_staff':
            return request.method in SAFE_METHODS

        return False
