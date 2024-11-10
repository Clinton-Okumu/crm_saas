from typing import Any, ClassVar, Dict
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from users.permissions import CRMModulePermission, BaseModulePermission

class CanManageCustomers(CRMModulePermission):
    """
    Permission class for managing customers within the CRM module.
    """
    module: str = 'crm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_customer': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_customer': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'update_customer': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_customer': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_customer',
            'POST': 'create_customer',
            'PUT': 'update_customer',
            'PATCH': 'update_customer',
            'DELETE': 'delete_customer'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_customer'))


class CanManageContacts(CRMModulePermission):
    """
    Permission class for managing contacts within the CRM module.
    """
    module: str = 'crm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_contact': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_contact': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'update_contact': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'delete_contact': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_contact',
            'POST': 'create_contact',
            'PUT': 'update_contact',
            'PATCH': 'update_contact',
            'DELETE': 'delete_contact'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_contact'))

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return self.has_action_permission(request, 'view_contact')
        
        action = 'delete_contact' if request.method == 'DELETE' else 'update_contact'
        return self.has_action_permission(request, action)


class CanManageInteractions(CRMModulePermission):
    """
    Permission class for managing interactions within the CRM module.
    """
    module: str = 'crm'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_interaction': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_interaction': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'update_interaction': BaseModulePermission.ROLE_HIERARCHY['manager'],
        'delete_interaction': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'manage_own_interaction': BaseModulePermission.ROLE_HIERARCHY['staff'],
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not super().has_permission(request, view):
            return False
            
        action_mapping = {
            'GET': 'view_interaction',
            'POST': 'create_interaction',
            'PUT': 'update_interaction',
            'PATCH': 'update_interaction',
            'DELETE': 'delete_interaction'
        }
        return self.has_action_permission(request, action_mapping.get(request.method, 'view_interaction'))

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user
        
        # Check if user owns the interaction
        is_owner = hasattr(obj, 'created_by') and obj.created_by == user
        
        if is_owner:
            return self.has_action_permission(request, 'manage_own_interaction')
            
        if request.method in SAFE_METHODS:
            return self.has_action_permission(request, 'view_interaction')
        
        action = 'delete_interaction' if request.method == 'DELETE' else 'update_interaction'
        return self.has_action_permission(request, action)
