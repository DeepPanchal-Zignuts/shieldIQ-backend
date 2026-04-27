"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

api_v1_patterns = [
    path("auth/", include("apps.users.urls.auth_urls")),
    path("medias/", include("apps.medias.urls.media_urls")),
    path("users/", include("apps.users.urls.user_urls")),
    path("events/", include("apps.events.urls.event_urls")),
    path("users/simulation/", include("apps.campaigns.urls.simulation_urls")),
    # ─── Admin Only ────────────────────────────────────────────────────────
    path("admin/users/", include("apps.users.urls.admin_urls")),  # list, retrieve
    path("admin/campaigns/", include("apps.campaigns.urls.campaign_urls")),
    path("admin/stats/", include("apps.events.urls.stats_urls")),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
]
