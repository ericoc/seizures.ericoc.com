from django.urls import include, path

from .api import api_router
from .views.date import SeizuresSearchDateView
from .views.ssid import SeizuresSSIDView


urlpatterns = [
    path("", SeizuresSearchDateView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path("ssid/<str:search_ssid>/", SeizuresSSIDView.as_view(), name="ssid"),
]
