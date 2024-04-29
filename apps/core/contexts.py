from django.conf import settings


def sentry_js(request):
    """Context processor for Sentry JavaScript."""
    val = None
    if settings.DEBUG is False:
        val = settings.SENTRY.get("USER") or None
    return {"SENTRY_JS": val}


def website_title(request):
    """Context processor for website title."""
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
