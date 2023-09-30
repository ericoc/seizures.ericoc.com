from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from seizures.views import (
    APIUserViewSet, APIGroupViewSet, APISeizureViewSet,
    SeizureAllView, SeizureSinceView,
    SeizureYearView, SeizureMonthView, SeizureDayView
)


api_router = routers.DefaultRouter()
api_router.register(r"users", APIUserViewSet)
api_router.register(r"groups", APIGroupViewSet)
api_router.register(r"seizures", APISeizureViewSet)

# Automatic URL routing.
urlpatterns = [

    path('admin/', admin.site.urls, name="admin"),
    path('api/', include(api_router.urls), name="api"),
    path('all/', SeizureAllView.as_view(), name="all"),

    path("", SeizureSinceView.as_view(), name="index"),

    path("minutes/<int:minutes>/", SeizureSinceView.as_view(), name="minutes"),
    path("hours/<int:hours>/", SeizureSinceView.as_view(), name="hours"),
    path("days/<int:days>/", SeizureSinceView.as_view(), name="days"),
    path("weeks/<int:weeks>/", SeizureSinceView.as_view(), name="weeks"),
    path("years/<int:years>/", SeizureSinceView.as_view(), name="years"),

    path('<int:year>/', SeizureYearView.as_view(), name="year"),
    path("<int:year>/<int:month>/", SeizureMonthView.as_view(), name="month"),
    path("<int:year>/<int:month>/<int:day>/", SeizureDayView.as_view(), name="day")
]
