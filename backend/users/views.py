from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema  # Import Swagger utilities
from drf_yasg import openapi
from .models import CustomUser
from .serializers import CustomUserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    @swagger_auto_schema(
        operation_summary="list users",
        operation_description="Retrieve all users based on the authenticated user's role.",
        responses={200: CustomUserSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.role == CustomUser.Role.ADMIN:
            return CustomUser.objects.all()
        elif self.request.user.role == CustomUser.Role.MANAGER:
            return CustomUser.objects.filter(role=CustomUser.Role.CLIENT)
        return CustomUser.objects.none()

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve or update the profile",
        operation_description="Retrieve or update the profile of the authenticated user.",
        responses={200: UserProfileSerializer()},
    )
    def get_object(self):
        return self.request.user.profile
