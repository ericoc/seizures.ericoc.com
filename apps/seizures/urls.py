from django.urls import include, path

from .api import api_router
from .views import SeizuresView, TableView


urlpatterns = [
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path("table/", TableView.as_view(), name="table")
]
