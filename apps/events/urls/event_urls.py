from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.events.controllers.campaign_event_controller import CampaignEventsController


# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", CampaignEventsController, basename="events")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path("", include(router.urls)),
]
