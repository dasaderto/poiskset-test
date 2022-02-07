from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.app.http.requests.auth_requests import LoginRequest, RegisterRequest
from core.app.http.resources.user_resources import UserResource
from core.app.services.auth_service import LoginUser, RegisterUser, RegisterUserData, VerifyUser


class LoginHandler(GenericAPIView):
    serializer_class = LoginRequest

    def post(self, *args, **kwargs):
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        token_data = LoginUser(email=data.validated_data['email'], password=data.validated_data['password']).login()

        return Response({
            'data': token_data
        })


class RegisterHandler(GenericAPIView):
    serializer_class = RegisterRequest

    def post(self, *args, **kwargs):
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        user, tokens = RegisterUser(data=RegisterUserData(
            first_name=data.validated_data['first_name'],
            last_name=data.validated_data['last_name'],
            email=data.validated_data['email'],
            password=data.validated_data['password'],
        )).register()

        return Response({
            'data': {
                'user': UserResource(user).data,
                'tokens': tokens,
            }
        })


class VerifyEmailHandler(APIView):
    def get(self, request, token: str, *args, **kwargs):
        user = VerifyUser(email_verify_token=token).verify()

        return Response({
            'data': UserResource(user).data
        })
