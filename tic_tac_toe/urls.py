"""
URL configuration for tic_tac_toe project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/games/", include("games.urls")),
    path("api/players/", include("players.urls")),
]
