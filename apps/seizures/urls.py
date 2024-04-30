from django.urls import include, path

from .api import api_router
from .views import SeizuresView


urlpatterns = [
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path(
        "table/", SeizuresView.as_view(template_name="table.html"), name="table"
    ),
]
