from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema  # Import Swagger utilities
from drf_yasg import openapi  # Import for manual parameters

from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from users.models import CustomUser


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user with email, username, company, role, and password",
        responses={201: "User created successfully", 400: "Invalid data"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "User created successfully",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "company": user.company,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "User creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Custom Login View (JWT-based)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description="Obtain JWT token pair (access and refresh) by providing valid credentials",
        responses={200: "Login successful", 401: "Unauthorized"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Logout View
class LogoutView(APIView):
    @swagger_auto_schema(
        operation_summary="Logout user",
        operation_description="Logout user by blacklisting the provided refresh token",
        manual_parameters=[
            openapi.Parameter('refresh_token', openapi.IN_BODY, description="Refresh token to blacklist", type=openapi.TYPE_STRING)
        ],
        responses={205: "Logout successful", 400: "Invalid token or token not provided"}
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": "success",
                "message": "Logout successful"
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Invalid token or token not provided",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
