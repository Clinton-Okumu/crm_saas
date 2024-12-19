from enum import Enum
from typing import Dict, Optional, Any, ClassVar
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from users.models import CustomUser


class Action(Enum):
    """
    Enum to hold all possible actions
    """

    CREATE = "POST"
    READ = "GET"
    UPDATE = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseModulePermission(BasePermission):
    """
    Base permission class that handles module access and role hierarchy.
    Provides a foundation for module-specific permissions with role-based access control.
    """

    module: Optional[str] = None
    admin_role: Optional[str] = None
    manager_role: Optional[str] = None
    staff_role: Optional[str] = None

    # Central role hierarchy for all modules
    ROLE_HIERARCHY: ClassVar[Dict[str, int]] = {
        "super_admin": 4,  # Highest level
        "admin": 3,
        "manager": 2,
        "staff": 1,  # Lowest level
    }

    def has_module_access(self, user: CustomUser) -> bool:
        """Check if the user has access to the specified module."""
        return bool(
            user and user.is_authenticated and self.module in user.accessible_modules
        )

    def get_role_level(self, user: CustomUser) -> int:
        """Retrieve the user's level based on their role in the module hierarchy."""
        if user.role == "super_admin":
            return self.ROLE_HIERARCHY["super_admin"]
        elif user.role == self.admin_role:
            return self.ROLE_HIERARCHY["admin"]
        elif user.role == self.manager_role:
            return self.ROLE_HIERARCHY["manager"]
        elif user.role == self.staff_role:
            return self.ROLE_HIERARCHY["staff"]
        return 0

    def _get_action(self, request: Request, view: APIView) -> str:
        """Helper function to get the action from view or request method."""
        if hasattr(view, "action") and view.action:
            return view.action
        return request.method

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Determine if the user has general access permissions for the view based on role level.
        """
        if not self.has_module_access(request.user):
            return False

        action = self._get_action(request, view)
        user_level = self.get_role_level(request.user)

        # Super admin and module admin have full access
        if user_level >= self.ROLE_HIERARCHY["admin"]:
            return True

        # Managers can do everything except DELETE
        if user_level >= self.ROLE_HIERARCHY["manager"]:
            return action != Action.DELETE.value

        # Staff have read-only access
        return action in SAFE_METHODS

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        """
        Determine if the user has specific permissions to interact with an object.
        """
        if not self.has_module_access(request.user):
            return False

        user_level = self.get_role_level(request.user)
        action = self._get_action(request, view)

        # Super admin and module admin have full access
        if user_level >= self.ROLE_HIERARCHY["admin"]:
            return True

        # Managers can modify but not delete
        if user_level >= self.ROLE_HIERARCHY["manager"]:
            if action == Action.DELETE.value:
                return False
            try:
                if (
                    hasattr(obj, "role")
                    and self.get_role_level(obj) >= self.ROLE_HIERARCHY["admin"]
                ):
                    return False
            except AttributeError:
                pass
            return True

        # Staff have read-only access
        if action in SAFE_METHODS:
            return True

        # Users can always modify their own records
        try:
            try:
                return (hasattr(obj, "user_id") and obj.user_id == request.user.id) or (
                    hasattr(obj, "employee_id") and obj.employee_id == request.user.id
                )
            except AttributeError:
                return False
        except ObjectDoesNotExist:
            return False


class HRModulePermission(BaseModulePermission):
    """
    Permission class for HR module with specific role hierarchy.
    """

    module: str = "hrm"
    admin_role: str = "hr_admin"
    manager_role: str = "hr_manager"
    staff_role: str = "hr_staff"

    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        "create_department": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "modify_department": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_department": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_employee": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "modify_employee": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "view_employee": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "manage_salary": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_salary": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "create_leave": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "approve_leave": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "view_leave": BaseModulePermission.ROLE_HIERARCHY["staff"],
    }

    def get_required_level(self, action: str) -> int:
        """
        Define the minimum role level required for specific actions.
        Falls back to admin level if action is not defined.
        """
        return self.ACTION_LEVELS.get(
            action, BaseModulePermission.ROLE_HIERARCHY["admin"]
        )

    def has_action_permission(self, request: Request, action: str) -> bool:
        """
        Check if user has permission for a specific action within the HR module.
        """
        user_level = self.get_role_level(request.user)
        required_level = self.get_required_level(action)
        return user_level >= required_level


class CRMModulePermission(BaseModulePermission):
    """
    Permission class for CRM module with specific role hierarchy.
    """

    module: str = "crm"
    admin_role: str = "crm_admin"
    manager_role: str = "crm_manager"
    staff_role: str = "sales_rep"

    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        "create_customer": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "modify_customer": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_customer": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_sales_record": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "view_sales_record": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_sales_record": BaseModulePermission.ROLE_HIERARCHY["manager"],
        "view_dashboard": BaseModulePermission.ROLE_HIERARCHY["staff"],
    }

    def get_required_level(self, action: str) -> int:
        """
        Define the minimum role level required for specific actions.
        Falls back to admin level if action is not defined.
        """
        return self.ACTION_LEVELS.get(
            action, BaseModulePermission.ROLE_HIERARCHY["admin"]
        )

    def has_action_permission(self, request: Request, action: str) -> bool:
        """
        Check if user has permission for a specific action within the CRM module.
        """
        user_level = self.get_role_level(request.user)
        required_level = self.get_required_level(action)
        return user_level >= required_level


class AccModulePermission(BaseModulePermission):
    """
    Permission class for the Accounting module with specific role hierarchy.
    """

    module: str = "accounting"
    admin_role: str = "accounting_admin"
    staff_role: str = "accountant"

    # Define action levels required for specific tasks in the accounting module
    ACTION_LEVELS: ClassVar[Dict[str, int]] = {
        "view_account": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "modify_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_account": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_transaction": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_transaction": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_transaction": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_transaction": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_invoice": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_invoice": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_invoice": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_invoice": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "view_payment": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "create_payment": BaseModulePermission.ROLE_HIERARCHY["staff"],
        "modify_payment": BaseModulePermission.ROLE_HIERARCHY["admin"],
        "delete_payment": BaseModulePermission.ROLE_HIERARCHY["admin"],
    }

    def get_required_level(self, action: str) -> int:
        """
        Get the minimum role level required for specific actions.
        Falls back to admin level if action is not defined.
        """
        return self.ACTION_LEVELS.get(
            action, BaseModulePermission.ROLE_HIERARCHY["admin"]
        )

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Check if the user has general permissions for the requested action.
        """
        if not self.has_module_access(request.user):
            return False

        action = self._get_action(request, view)
        user_level = self.get_role_level(request.user)
        required_level = self.get_required_level(action)

        return user_level >= required_level

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        """
        Check if the user has permissions to interact with a specific object.
        """
        if not self.has_module_access(request.user):
            return False

        user = request.user
        action = self._get_action(request, view)
        user_level = self.get_role_level(user)

        if action == Action.DELETE.value and user_level < self.ROLE_HIERARCHY["admin"]:
            return False

        if (
            action in [Action.UPDATE.value, Action.PATCH.value]
            and user.role == self.staff_role
        ):
            try:
                return obj.created_by == user
            except AttributeError:
                return False

        return True
