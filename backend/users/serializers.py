# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Your existing serializers
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'department', 'position', 'bio', 'date_of_birth']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'company', 'role', 'role_display',
            'primary_module', 'accessible_modules', 'profile',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['accessible_modules', 'date_joined']

class UserCreateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'password', 'company', 'role', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
            
        return user

# Add these new serializers for dj-rest-auth
class CustomUserDetailsSerializer(UserSerializer):
    """
    Serializer for returning the user details to dj-rest-auth
    """
    class Meta(UserSerializer.Meta):
        pass

class CustomRegisterSerializer(UserCreateSerializer):
    """
    Serializer for user registration with dj-rest-auth
    """
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ['password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return super().create(validated_data)
