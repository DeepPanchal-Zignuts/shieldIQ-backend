from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.events.controllers.campaign_stats_controller import CampaignStatsController


# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", CampaignStatsController, basename="stats")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [
    path("", include(router.urls)),
]
