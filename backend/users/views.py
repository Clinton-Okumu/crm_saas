from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserSerializer, UserCreateSerializer, UserProfileSerializer
from .permissions import CanManageUsers

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CanManageUsers]
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Super admin sees all users
        if user.role == 'super_admin':
            return User.objects.all()
            
        # HR admin sees all except super admin
        if user.role == 'hr_admin':
            return User.objects.exclude(role='super_admin')
            
        # Module admins see users in their module
        if user.role.endswith('_admin'):
            module = user.primary_module
            return User.objects.filter(accessible_modules__contains=[module])
            
        # Others only see themselves
        return User.objects.filter(id=user.id)

    @action(detail=True, methods=['patch'])
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})