from django.contrib import admin
from django.urls import include, path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("sentry-debug/", trigger_error, name="trigger_error"),
    path("", include("seizures.urls"), name="seizures")
]
