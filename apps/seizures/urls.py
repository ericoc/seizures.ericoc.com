from django.urls import include, path

from .api import api_router
from .views import \
    SeizuresView, SeizuresChartjsView, SeizuresHighchartsView, SeizuresTableView


urlpatterns = [

    # Main Leaflet map.
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),

    # TODO: Improve Chart.js and link to it, or go all in on Highcharts?
    path("chartjs/", SeizuresChartjsView.as_view(), name="chartjs"),

    # Highcharts.
    path("highcharts/", SeizuresHighchartsView.as_view(), name="highcharts"),

    # DataTable.
    path("table/", SeizuresTableView.as_view(), name="table")
]
