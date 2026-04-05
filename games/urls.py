from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GameViewSet

router = DefaultRouter()
router.register(r"", GameViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
