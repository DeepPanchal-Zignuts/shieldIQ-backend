from django.urls import path
from rest_framework.permissions import IsAuthenticated

from apps.users.controllers.user_controller import UserController

urlpatterns = [
    path(
        "me/",
        UserController.as_view(
            {"get": "get_user_profile_details"},
            permission_classes=[IsAuthenticated],
        ),
        name="user-me",
    ),
    path(
        "stats/",
        UserController.as_view(
            {"get": "get_user_stats"},
            permission_classes=[IsAuthenticated],
        ),
        name="user-stats",
    ),
]
