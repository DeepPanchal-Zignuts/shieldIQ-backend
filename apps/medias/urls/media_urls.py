from django.urls import path
from rest_framework.permissions import IsAuthenticated

from apps.medias.controllers.media_controller import MediaController

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "upload-single/",
        MediaController.as_view(
            {"post": "upload_single_media"},
            permission_classes=[IsAuthenticated],
        ),
        name="upload_single_media",
    ),
    path(
        "<uuid:pk>/",
        MediaController.as_view(
            {"delete": "delete_single_media"},
            permission_classes=[IsAuthenticated],
        ),
        name="delete_single_media",
    ),
]
