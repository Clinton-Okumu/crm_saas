from typing import Any, ClassVar, Dict
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from users.permissions import BaseModulePermission, AccModulePermission

class CanManageAccounts(AccModulePermission):
    """
    Permission class for managing accounts within the accounting module.
    """
    module: str = 'accounting'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_account': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_account': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'modify_account': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_account': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            'GET': 'view_account',
            'POST': 'create_account',
            'PUT': 'modify_account',
            'PATCH': 'modify_account',
            'DELETE': 'delete_account'
        }
        action = action_mapping.get(request.method)
        return self.has_action_permission(request, action)

class CanManageTransactions(AccModulePermission):
    """
    Permission class for managing transactions within the accounting module.
    """
    module: str = 'accounting'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_transaction': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_transaction': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'modify_transaction': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_transaction': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            'GET': 'view_transaction',
            'POST': 'create_transaction',
            'PUT': 'modify_transaction',
            'PATCH': 'modify_transaction',
            'DELETE': 'delete_transaction'
        }
        action = action_mapping.get(request.method)
        return self.has_action_permission(request, action)

class CanManageInvoices(AccModulePermission):
    """
    Permission class for managing invoices within the accounting module.
    """
    module: str = 'accounting'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_invoice': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_invoice': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'modify_invoice': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_invoice': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            'GET': 'view_invoice',
            'POST': 'create_invoice',
            'PUT': 'modify_invoice',
            'PATCH': 'modify_invoice',
            'DELETE': 'delete_invoice'
        }
        action = action_mapping.get(request.method)
        return self.has_action_permission(request, action)

class CanManagePayments(AccModulePermission):
    """
    Permission class for managing payments within the accounting module.
    """
    module: str = 'accounting'
    
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        'view_payment': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'create_payment': BaseModulePermission.ROLE_HIERARCHY['staff'],
        'modify_payment': BaseModulePermission.ROLE_HIERARCHY['admin'],
        'delete_payment': BaseModulePermission.ROLE_HIERARCHY['admin'],
    }
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            'GET': 'view_payment',
            'POST': 'create_payment',
            'PUT': 'modify_payment',
            'PATCH': 'modify_payment',
            'DELETE': 'delete_payment'
        }
        action = action_mapping.get(request.method)
        return self.has_action_permission(request, action)
