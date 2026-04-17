from django.urls import path, include

# Base user url patterns
urlpatterns = [
    path("auth/", include("apps.users.urls.auth_urls")),
    path("profile/", include("apps.users.urls.profile_urls")),
]
