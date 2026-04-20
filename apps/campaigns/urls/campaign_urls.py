from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.campaigns.controllers.campaign_controller import CampaignController

# Create a router using the DefaultRouter
router = DefaultRouter(trailing_slash=True)
router.register(r"", CampaignController, basename="campaigns")

# The `urlpatterns` list routes URLs to controllers functions
urlpatterns = [path("", include(router.urls))]
