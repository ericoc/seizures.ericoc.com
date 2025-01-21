from django.urls import include, path

from .api import api_router
from .views import SeizuresView, ChartView, TableView


urlpatterns = [
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path("chart/", ChartView.as_view(), name="chart"),
    path("table/", TableView.as_view(), name="table")
]
