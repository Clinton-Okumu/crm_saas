from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, PasswordChangeSerializer
from .authentication.throttling import LoginRateThrottle

class LoginView(TokenObtainPairView):
    """
    Login view that returns JWT tokens and user info
    """
    throttle_classes = [LoginRateThrottle]
    serializer_class = LoginSerializer

class LogoutView(APIView):
    """
    Logout view that blacklists the refresh token
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid token."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordChangeView(APIView):
    """
    View for changing user password
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response(
                    {"detail": "Password updated successfully."}, 
                    status=status.HTTP_200_OK
                )
            return Response(
                {"detail": "Invalid old password."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    """
    View for refreshing access tokens
    """
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token."}, 
                status=status.HTTP_400_BAD_REQUEST
            )