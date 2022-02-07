from django.urls import path

from core.app.handlers.auth_handler import LoginHandler, RegisterHandler, VerifyEmailHandler

urlpatterns = [
    path('login/', LoginHandler.as_view()),
    path('register/', RegisterHandler.as_view()),
    path('verify/email/<str:token>/', VerifyEmailHandler.as_view()),
]
