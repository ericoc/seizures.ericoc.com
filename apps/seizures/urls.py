from django.urls import include, path

from .api import api_router
from .views import (
    SeizuresMainView,
    SeizuresCalendarView, SeizuresChartView, SeizuresMapView, SeizuresTableView
)


urlpatterns = [

    # Home.
    path("", SeizuresMainView.as_view(), name="main"),

    # Django REST framework.
    path("api/", include(api_router.urls), name="api"),

    # fullcalendar.
    path("calendar/", SeizuresCalendarView.as_view(), name="calendar"),

    # Highcharts.
    path("chart/", SeizuresChartView.as_view(), name="chart"),

    # Leaflet.
    path("map/", SeizuresMapView.as_view(), name="map"),

    # DataTables.
    path("table/", SeizuresTableView.as_view(), name="table")
]
