from .views import SeizuresErrorView


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
handler503 = SeizuresErrorView.as_view(
    message="Sorry, but unfortunately, the service is currently not reachable.",
    status_code=503
)
