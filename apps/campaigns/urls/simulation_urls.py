from django.urls import path
from rest_framework.permissions import IsAuthenticated
from apps.campaigns.controllers.campaign_email_controller import CampaignEmailController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    # GET /api/v1/users/simulation/
    path(
        "",
        CampaignEmailController.as_view(
            {"get": "list"},
            permission_classes=[IsAuthenticated],
        ),
        name="user-simulation",
    ),
    # GET /api/v1/users/simulation/campaigns/
    path(
        "campaigns/",
        CampaignEmailController.as_view(
            {"get": "list_simulation_campaigns"},
            permission_classes=[IsAuthenticated],
        ),
        name="user-simulation-campaigns",
    ),
]
