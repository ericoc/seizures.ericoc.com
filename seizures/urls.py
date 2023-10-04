from django.urls import path

from seizures.views import (
    SeizureLoginView, SeizureLogoutView,
    SeizureAllView, SeizureSinceView,
    SeizureYearView, SeizureMonthView, SeizureDayView
)


urlpatterns = [

    path("", SeizureSinceView.as_view(), name="index"),

    path("all/", SeizureAllView.as_view(), name="all"),

    path("login/", SeizureLoginView.as_view(), name="login"),
    path("logout/", SeizureLogoutView.as_view(), name="logout"),

    path("minutes/<int:minutes>/", SeizureSinceView.as_view(), name="minutes"),
    path("hours/<int:hours>/", SeizureSinceView.as_view(), name="hours"),
    path("days/<int:days>/", SeizureSinceView.as_view(), name="days"),
    path("weeks/<int:weeks>/", SeizureSinceView.as_view(), name="weeks"),
    path("months/<int:months>/", SeizureSinceView.as_view(), name="months"),
    path("years/<int:years>/", SeizureSinceView.as_view(), name="years"),

    path('<int:year>/', SeizureYearView.as_view(), name="year"),
    path("<int:year>/<int:month>/", SeizureMonthView.as_view(), name="month"),
    path("<int:year>/<int:month>/<int:day>/", SeizureDayView.as_view(), name="day")
]
