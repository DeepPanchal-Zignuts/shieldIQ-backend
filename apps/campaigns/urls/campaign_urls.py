from django.urls import path
from rest_framework.permissions import IsAdminUser

from apps.campaigns.controllers.campaign_controller import CampaignController
from apps.campaigns.controllers.campaign_email_controller import CampaignEmailController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "",
        CampaignController.as_view(
            {"get": "list", "post": "create"},
            permission_classes=[IsAdminUser],
        ),
        name="campaigns",
    ),
    path(
        "<uuid:pk>/",
        CampaignController.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"},
            permission_classes=[IsAdminUser],
        ),
        name="campaigns-detail",
    ),
    path(
        "<uuid:campaign_id>/emails/",
        CampaignEmailController.as_view(
            {
                "post": "create_campaign_email",
            },
            permission_classes=[IsAdminUser],
        ),
    ),
]
