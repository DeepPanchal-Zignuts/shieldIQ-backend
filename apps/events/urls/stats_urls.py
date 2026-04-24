from django.urls import path
from rest_framework.permissions import IsAdminUser

from apps.events.controllers.campaign_stats_controller import CampaignStatsController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "",
        CampaignStatsController.as_view(
            {"get": "list"},
            permission_classes=[IsAdminUser],
        ),
        name="stats-list",
    ),
]
