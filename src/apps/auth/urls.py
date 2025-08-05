from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
    UserPublicProfileView
)


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("public-profile/<int:pk>/", UserPublicProfileView.as_view(), name="user-public-profile"),
]