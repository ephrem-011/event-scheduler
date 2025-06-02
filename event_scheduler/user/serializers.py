from rest_framework import serializers
from user.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        try:
            username_owner = User.objects.get(username = value)
        except User.DoesNotExist:
            return value
        else:
            if User.objects.filter(username=value).exists() and username_owner != self.instance:
                raise serializers.ValidationError("This username is already taken.")
            return value
    
    username = serializers.CharField(
        required=True,
        error_messages={
            "required": "User name is required.",
            "blank": "User name cannot be blank.",
        }
    )

    password = serializers.CharField(
        required=True,
        write_only = True,
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be blank.",
        }
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    def update(self, instance, validated_data):
        pwd = validated_data.get('password')
        instance.set_password(pwd)
        validated_data['password'] = instance.password
        return super().update(instance, validated_data)
