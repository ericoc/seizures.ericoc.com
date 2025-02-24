from django.urls import include, path

from .api import api_router
from .views import \
    SeizuresView, SeizuresChartjsView, SeizuresHighchartsView, SeizuresTableView


urlpatterns = [
    path("", SeizuresView.as_view(), name="seizures"),
    path("api/", include(api_router.urls), name="api"),
    path("chartjs/", SeizuresChartjsView.as_view(), name="chartjs"),
    path("highcharts/", SeizuresHighchartsView.as_view(), name="highcharts"),
    path("table/", SeizuresTableView.as_view(), name="table")
]
