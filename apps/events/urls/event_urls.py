from django.urls import path
from rest_framework.permissions import IsAuthenticated

from apps.events.controllers.campaign_event_controller import CampaignEventsController


# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path(
        "track/",
        CampaignEventsController.as_view(
            {"post": "create_campaign_event"},
            permission_classes=[IsAuthenticated],
        ),
        name="event-create",
    ),
]
