from django.urls import include, path

from .api import api_router
from .views import SeizuresView, SeizuresChartView, SeizuresTableView


urlpatterns = [
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path("chart/", SeizuresChartView.as_view(), name="chart"),
    path("table/", SeizuresTableView.as_view(), name="table")
]
