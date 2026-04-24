from django.urls import path
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.controllers.auth_controller import AuthController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "register/",
        AuthController.as_view(
            {"post": "register_user"},
            permission_classes=[AllowAny],
        ),
        name="auth-register",
    ),
    path(
        "login/",
        AuthController.as_view(
            {"post": "login_user"},
            permission_classes=[AllowAny],
        ),
        name="auth-login",
    ),
    path(
        "verify-email/",
        AuthController.as_view(
            {"post": "verify_email"},
            permission_classes=[AllowAny],
        ),
        name="auth-verify-email",
    ),
    path(
        "forgot-password/",
        AuthController.as_view(
            {"post": "forgot_password"},
            permission_classes=[AllowAny],
        ),
        name="auth-forgot-password",
    ),
    path(
        "reset-password/",
        AuthController.as_view(
            {"post": "reset_password"},
            permission_classes=[AllowAny],
        ),
        name="auth-reset-password",
    ),
    path(
        "logout/",
        AuthController.as_view(
            {"post": "logout"},
            permission_classes=[IsAuthenticated],
        ),
        name="auth-logout",
    ),
]
