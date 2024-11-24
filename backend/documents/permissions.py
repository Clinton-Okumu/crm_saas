from rest_framework import permissions

class IsDocumentAccessAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        # First level check - is user authenticated?
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Allow if user is document owner
        if obj.created_by == user:
            return True
            
        # Allow if document is public and request is read-only
        if obj.is_public and request.method in permissions.SAFE_METHODS:
            return True
            
        # Check if user has specific share permissions
        share = obj.documentshare_set.filter(user=user).first()
        if share:
            if share.permission == 'full':
                return True
            if share.permission == 'edit' and request.method in ['GET', 'PUT', 'PATCH']:
                return True
            if share.permission == 'view' and request.method in permissions.SAFE_METHODS:
                return True
                
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
