from dataclasses import dataclass
from typing import Tuple

from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from core.models import User, AuthToken
from core.tasks import html_email_sender


class LoginUser:
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password

    def login(self) -> AuthToken:
        user = User.objects.filter(email=self._email).first()
        if not user:
            raise NotFound(f"Undefined user with email {self._email}")

        if not user.check_password(self._password):
            raise PermissionDenied("Failed auth data")

        tokens = user.get_tokens_for_user()
        return tokens


@dataclass
class RegisterUserData:
    first_name: str
    last_name: str
    email: str
    password: str


class RegisterUser:
    _user: User = None

    def __init__(self, data: RegisterUserData):
        self._data = data

    @property
    def user(self):
        if not self._user:
            user = User()
            user.first_name = self._data.first_name
            user.last_name = self._data.last_name
            user.email = self._data.email
            user.username = self._data.email
            user.email_verify_token = get_random_string(40)
            user.set_password(self._data.password)
            self._user = user
        return self._user

    def _check_perms(self):
        exists_user = User.objects.filter(email=self._data.email).exists()
        if exists_user:
            raise ValidationError(f"User with email {self._data.email} already exists")

    def register(self) -> Tuple[User, AuthToken]:
        self._check_perms()
        self.user.save()
        html_email_sender.delay(subject="Register verify",
                                content=f"Verify token {self.user.email_verify_token}",
                                html_content="<span><b>Тут мог бы быть html, но его надо сверстать</b></span>",
                                message_from=settings.EMAIL_FROM,
                                emails=[self.user.email])
        return self.user, self.user.get_tokens_for_user()


class VerifyUser:
    def __init__(self, email_verify_token: str):
        self._token = email_verify_token

    def verify(self) -> User:
        user = User.objects.filter(email_verify_token=self._token).first()
        if not user:
            raise NotFound("Failed verify_token")

        user.email_verified = True
        user.save()

        html_email_sender.delay(subject="Success email verification",
                                content="Hello, your email was success verified",
                                html_content="<span><b>Тут мог бы быть html, но его надо сверстать</b></span>",
                                message_from=settings.EMAIL_FROM,
                                emails=[user.email])

        return user
