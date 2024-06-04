from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static

from apps.core.errors import *
from apps.users.views import SeizuresLoginView, SeizuresLogoutView


def trigger_error(request):
    return 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("sentry-debug/", trigger_error, name="trigger_error"),
    path("", include("apps.seizures.urls"), name="seizures"),
    path("login/", SeizuresLoginView.as_view(), name="login"),
    path("logout/", SeizuresLogoutView.as_view(), name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += path("400/", handler400, name="400"),
    urlpatterns += path("401/", handler401, name="401"),
    urlpatterns += path("403/", handler403, name="403"),
    urlpatterns += path("404/", handler404, name="404"),
    urlpatterns += path("405/", handler405, name="405"),
    urlpatterns += path("410/", handler410, name="410"),
    urlpatterns += path("420/", handler420, name="420"),
    urlpatterns += path("500/", handler500, name="500"),
    urlpatterns += path("501/", handler501, name="501"),
    urlpatterns += path("503/", handler503, name="503"),
