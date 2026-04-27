from django.urls import path
from rest_framework.permissions import IsAuthenticated
from apps.campaigns.controllers.campaign_email_controller import CampaignEmailController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "",
        CampaignEmailController.as_view(
            {"get": "list"},
            permission_classes=[IsAuthenticated],
        ),
        name="user-simulation",
    ),
]
