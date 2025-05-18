from django.urls import include, path

from .api import api_router
from .views import (
    SeizuresMainView, SeizuresChartView, SeizuresMapView, SeizuresTableView
)


urlpatterns = [

    # Home.
    path("", SeizuresMainView.as_view(), name="map"),

    # Django REST framework.
    path("api/", include(api_router.urls), name="api"),

    # Highcharts.
    path("chart/", SeizuresChartView.as_view(), name="chart"),

    # Leaflet.
    path("map/", SeizuresMapView.as_view(), name="map"),

    # DataTables.
    path("table/", SeizuresTableView.as_view(), name="table")
]
