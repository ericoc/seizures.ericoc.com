from django.conf import settings


def sentry_js(request):
    """Context processor for Sentry JavaScript."""
    return {"SENTRY_JS": settings.SENTRY.get("USER") or None}


def website_title(request):
    """Context processor for website title."""
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
