from django.urls import include, path

from .api import api_router
from .views import SeizuresView, SeizureChartView, SeizuresTableView


urlpatterns = [

    # Main Leaflet map.
    path("", SeizuresView.as_view(), name="seizures"),

    # Django REST Framework.
    path("api/", include(api_router.urls), name="api"),

    # Highcharts.
    path("chart/", SeizureChartView.as_view(), name="chart"),

    # DataTables.
    path("table/", SeizuresTableView.as_view(), name="table")
]
