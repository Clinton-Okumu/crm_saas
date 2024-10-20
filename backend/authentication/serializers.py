from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'company', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            company=validated_data.get('company', ''),
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user

# Custom serializer for login to include additional user info in the token response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'role': self.user.role,
            'company': self.user.company,
        })
        return data
