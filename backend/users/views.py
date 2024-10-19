from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from .permissions import IsAdminUser, IsManagerUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile