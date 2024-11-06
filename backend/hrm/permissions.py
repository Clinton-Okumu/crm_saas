from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.permissions import IsSuperAdmin, IsHRAdmin, CanManageUsers

class BaseHRMPermission(BasePermission):
   def has_permission(self, request, view):
       return bool(
           request.user and
           request.user.is_authenticated and 
           request.user.has_module_access('hrm')
       )

class CanManageDepartments(BaseHRMPermission):
   def has_permission(self, request, view):
       if not super().has_permission(request, view):
           return False
           
       if request.method in SAFE_METHODS:
           return request.user.role in ['hr_admin', 'hr_manager', 'hr_staff']
       return request.user.role == 'hr_admin'

class CanManageEmployees(BaseHRMPermission):
   def has_permission(self, request, view):
       if not super().has_permission(request, view):
           return False
           
       if request.method in SAFE_METHODS:
           return True
       return request.user.role in ['hr_admin', 'hr_manager']

   def has_object_permission(self, request, view, obj):
       user = request.user
       
       if user.role == 'hr_admin':
           return True
           
       if user.role == 'hr_manager':
           return obj.role not in ['hr_admin']
           
       if user.role == 'hr_staff':
           return obj.role not in ['hr_admin', 'hr_manager']
           
       return obj.id == user.id

class CanManageSalaries(BaseHRMPermission):
   def has_permission(self, request, view):
       if not super().has_permission(request, view):
           return False
           
       if request.method in SAFE_METHODS:
           return request.user.role in ['hr_admin', 'hr_manager']
       return request.user.role == 'hr_admin'

   def has_object_permission(self, request, view, obj):
       user = request.user
       
       if user.role == 'hr_admin':
           return True
       if user.role == 'hr_manager':
           return obj.employee.department in user.managed_departments
       return False

class CanManageLeaves(BaseHRMPermission):
   def has_permission(self, request, view):
       if not super().has_permission(request, view):
           return False
           
       if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
           return True
       return request.user.role in ['hr_admin', 'hr_manager']

   def has_object_permission(self, request, view, obj):
       user = request.user
       
       if user.role == 'hr_admin':
           return True
           
       if user.role == 'hr_manager':
           return obj.employee.department in user.managed_departments
           
       if user.role == 'hr_staff':
           return request.method in SAFE_METHODS
           
       return obj.employee.id == user.id