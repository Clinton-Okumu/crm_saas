from typing import ClassVar, Dict
from rest_framework.request import Request
from rest_framework.views import APIView
from users.permissions import BaseModulePermission


class AccModulePermission(BaseModulePermission):
    """
    Base permission class for the Accounting module with specific role hierarchy.
    """

    module: str = "accounting"
    admin_role: str = "accounting_admin"
    manager_role: str = "accounting_manager"  # Added manager role
    staff_role: str = "accountant"

    # Define action levels required for specific tasks in the accounting module
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        # Account permissions
        "view_account": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "modify_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        # Transaction permissions
        "view_transaction": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_transaction": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_transaction": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_transaction": BaseModulePermission.ROLE_HIERARCHY["admin"],
        # Invoice permissions
        "view_invoice": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_invoice": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_invoice": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_invoice": BaseModulePermission.ROLE_HIERARCHY["admin"],
        # Payment permissions
        "view_payment": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_payment": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_payment": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_payment": BaseModulePermission.ROLE_HIERARCHY["admin"],
    }

    def get_required_level(self, action: str) -> int:
        """Get the minimum role level required for specific actions."""
        return self.ACTION_LEVELS.get(
            action, BaseModulePermission.ROLE_HIERARCHY["admin"]
        )

    def has_action_permission(self, request: Request, action: str) -> bool:
        """Check if user has permission for a specific action."""
        if not self.has_module_access(request.user):
            return False
        user_level = self.get_role_level(request.user)
        required_level = self.get_required_level(action)
        return user_level >= required_level


class CanManageAccounts(AccModulePermission):
    """Permission class for managing accounts."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            "GET": "view_account",
            "POST": "create_account",
            "PUT": "modify_account",
            "PATCH": "modify_account",
            "DELETE": "delete_account",
        }
        action = action_mapping.get(request.method)
        if not action:
            return False
        return self.has_action_permission(request, action)


class CanManageTransactions(AccModulePermission):
    """Permission class for managing transactions."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            "GET": "view_transaction",
            "POST": "create_transaction",
            "PUT": "modify_transaction",
            "PATCH": "modify_transaction",
            "DELETE": "delete_transaction",
        }
        action = action_mapping.get(request.method)
        if not action:
            return False
        return self.has_action_permission(request, action)


class CanManageInvoices(AccModulePermission):
    """Permission class for managing invoices."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            "GET": "view_invoice",
            "POST": "create_invoice",
            "PUT": "modify_invoice",
            "PATCH": "modify_invoice",
            "DELETE": "delete_invoice",
        }
        action = action_mapping.get(request.method)
        if not action:
            return False
        return self.has_action_permission(request, action)


class CanManagePayments(AccModulePermission):
    """Permission class for managing payments."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        action_mapping = {
            "GET": "view_payment",
            "POST": "create_payment",
            "PUT": "modify_payment",
            "PATCH": "modify_payment",
            "DELETE": "delete_payment",
        }
        action = action_mapping.get(request.method)
        if not action:
            return False
        return self.has_action_permission(request, action)
