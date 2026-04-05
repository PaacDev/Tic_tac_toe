from django.urls import include, path

from .views import get_current_user, login_view, logout_view, register_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("current_user/", get_current_user, name="current_user"),
]
