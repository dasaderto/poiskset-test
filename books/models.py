from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel, User


class Book(TimeStampedModel):
    name = models.CharField(max_length=255)
    pages_count = models.PositiveIntegerField()
    has_cover = models.BooleanField()
    genre = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
