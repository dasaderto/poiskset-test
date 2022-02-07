from typing import Dict, TypedDict

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class AuthToken(TypedDict):
    refresh: str
    access: str


class User(AbstractUser):
    email_verify_token = models.CharField(max_length=50)
    email_verified = models.BooleanField(default=False)

    def get_tokens_for_user(self) -> AuthToken:
        refresh = RefreshToken.for_user(self)

        return AuthToken(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=False)
    updated_at = models.DateTimeField(auto_now=True, db_index=False)

    class Meta(object):
        abstract = True
        ordering = ['-id']
