from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.controllers.auth_controller import AuthController

# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", AuthController, basename="auth")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [path("auth/", include(router.urls))]
