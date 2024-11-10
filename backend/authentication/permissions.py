from rest_framework.permissions import BasePermission

class HasModuleAccess(BasePermission):
    """
    Verify if user has access to specific module
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        required_module = getattr(view, 'required_module', None)
        if not required_module:
            return True
            
        return required_module in request.user.accessible_modules

class HasRole(BasePermission):
    """
    Verify if user has required role
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        required_roles = getattr(view, 'required_roles', [])
        if not required_roles:
            return True
            
        return request.user.role in required_roles