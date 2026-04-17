from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.controllers.user_controller import UserController

# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", UserController, basename="users")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [path("", include(router.urls))]
