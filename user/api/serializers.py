from rest_framework import serializers
from user.models import CustomUser as User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            return data
        raise serializers.ValidationError("User not registered with this data")
