from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from seizures.views import api, all, date, since


api_router = routers.DefaultRouter()
api_router.register(r"users", api.APIUserViewSet)
api_router.register(r"groups", api.APIGroupViewSet)
api_router.register(r"seizures", api.APISeizureViewSet)

# Automatic URL routing.
urlpatterns = [

    path('admin/', admin.site.urls, name="admin"),
    path('api/', include(api_router.urls), name="api"),
    path('all/', all.SeizureAllView.as_view(), name="all"),

    path("", since.SeizureSinceView.as_view(), name="index"),

    path("minutes/<int:minutes>/", since.SeizureSinceView.as_view(), name="minutes"),
    path("hours/<int:hours>/", since.SeizureSinceView.as_view(), name="hours"),
    path("days/<int:days>/", since.SeizureSinceView.as_view(), name="days"),
    path("weeks/<int:weeks>/", since.SeizureSinceView.as_view(), name="weeks"),
    path("years/<int:years>/", since.SeizureSinceView.as_view(), name="years"),

    path('<int:year>/', date.SeizureYearView.as_view(), name="year"),
    path("<int:year>/<int:month>/", date.SeizureMonthView.as_view(), name="month"),
    path("<int:year>/<int:month>/<int:day>/", date.SeizureDayView.as_view(), name="day")
]
