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
    # ─── Public Auth ───────────────────────────────
    path("auth/", include("apps.users.urls.auth_urls")),
    # ─── User Facing ───────────────────────────────
    path("profile/", include("apps.users.urls.profile_urls")),
    path("events/", include("apps.events.urls.event_urls")),
    # path("api/v1/knowledge/", include("apps.knowledge.urls")),
    # ─── Admin Only ────────────────────────────────
    path("admin/users/", include("apps.users.urls.user_urls")),
    path("admin/campaigns/", include("apps.campaigns.urls.campaign_urls")),
    path("admin/stats/", include("apps.events.urls.stats_urls")),
]

# Root url patterns
urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
]
