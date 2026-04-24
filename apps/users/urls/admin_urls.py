from django.urls import path
from rest_framework.permissions import IsAdminUser

from apps.users.controllers.user_controller import UserController

urlpatterns = [
    path(
        "list/",
        UserController.as_view(
            {"get": "get_all_users"},
            permission_classes=[IsAdminUser],
        ),
        name="admin-user-list",
    ),
    path(
        "<uuid:pk>/",
        UserController.as_view(
            {"get": "retrieve"},
            permission_classes=[IsAdminUser],
        ),
        name="admin-user-detail",
    ),
]
