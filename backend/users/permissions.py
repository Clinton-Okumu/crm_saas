from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'manager'

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'client'
