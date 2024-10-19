from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from users.models import CustomUser

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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

# Custom Login View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout View
class LogoutView(APIView):
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
