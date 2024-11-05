from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom login serializer that includes additional user info in response
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra responses
        data.update({
            'email': self.user.email,
            'role': self.user.role,
            'primary_module': self.user.primary_module,
            'accessible_modules': self.user.accessible_modules
        })
        return data

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value