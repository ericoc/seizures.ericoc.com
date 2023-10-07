from django.urls import path

from seizures.views import (
    SeizuresLoginView, SeizuresLogoutView,
    SeizuresSearchDateView, SeizuresSSIDView
)


urlpatterns = [
    path("", SeizuresSearchDateView.as_view(), name="seizures"),
    path("ssid/<str:search_ssid>/", SeizuresSSIDView.as_view(), name="ssid"),

    path("login/", SeizuresLoginView.as_view(), name="login"),
    path("logout/", SeizuresLogoutView.as_view(), name="logout")
]
