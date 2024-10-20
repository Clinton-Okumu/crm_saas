from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == request.user.Role.ADMIN

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == request.user.Role.MANAGER

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == request.user.Role.CLIENT
