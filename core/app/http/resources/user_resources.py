from rest_framework import serializers

from core.models import User


class UserResource(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email_verified',
            'first_name',
            'last_name',
            'email',
        ]
