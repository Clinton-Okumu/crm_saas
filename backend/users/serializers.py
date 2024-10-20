from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role', 'company', 'profile']
        read_only_fields = ['id', 'email']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)
        if profile_data:
            UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user
