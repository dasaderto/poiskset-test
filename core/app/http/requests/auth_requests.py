from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.utils.serializers import UnimplementedSerializer


class LoginRequest(UnimplementedSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterRequest(UnimplementedSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    passwordConfirmation = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs["passwordConfirmation"]:
            raise ValidationError("password must be equivalent to password confirmation")

        return attrs
