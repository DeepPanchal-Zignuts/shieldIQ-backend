from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.controllers.profile_controller import ProfileController

# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", ProfileController, basename="profile")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [path("", include(router.urls))]
