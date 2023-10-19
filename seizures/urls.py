from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from seizures.views import (
    SeizuresErrorView, SeizuresLoginView, SeizuresLogoutView,
    SeizuresSearchDateView, SeizuresSSIDView
)


urlpatterns = [
    path("", SeizuresSearchDateView.as_view(), name="seizures"),
    path("ssid/<str:search_ssid>/", SeizuresSSIDView.as_view(), name="ssid"),

    path("login/", SeizuresLoginView.as_view(), name="login"),
    path("logout/", SeizuresLogoutView.as_view(), name="logout")
]

handler400 = SeizuresErrorView.as_view(
    message="Sorry, but the request was not understood.",
    status_code=400
)
handler401 = SeizuresErrorView.as_view(
    message="Sorry, but you do not have authorization to access this page.",
    status_code=401
)
handler403 = SeizuresErrorView.as_view(
    message="Sorry, but access to this page is forbidden.",
    status_code=403,
)
handler404 = SeizuresErrorView.as_view(
    message="Sorry, but no such page could be found.",
    status_code=404,
)
handler405 = SeizuresErrorView.as_view(
    message="Sorry, but the requested method is not supported.",
    status_code=405,
)
handler410 = SeizuresErrorView.as_view(
    message="Sorry, but that resource is gone.",
    status_code=410,
)
handler420 = SeizuresErrorView.as_view(
    message="Sorry, but please enhance your calm.",
    status_code=420,
)
handler500 = SeizuresErrorView.as_view(
    message= "Sorry, but unfortunately, there was an internal server error.",
    status_code=500
)
handler501 = SeizuresErrorView.as_view(
    message= "Sorry, but the server cannot handle your request.",
    status_code=501
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("400/", handler400, name="400"),
    urlpatterns += path("401/", handler401, name="401"),
    urlpatterns += path("403/", handler403, name="403"),
    urlpatterns += path("404/", handler404, name="404"),
    urlpatterns += path("405/", handler405, name="405"),
    urlpatterns += path("410/", handler410, name="410"),
    urlpatterns += path("420/", handler420, name="420"),
    urlpatterns += path("500/", handler500, name="500"),
    urlpatterns += path("501/", handler501, name="501"),
