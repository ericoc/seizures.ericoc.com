from django.conf import settings


def device_icons(request):
    # Context processor for device icons.
    return {"DEVICE_ICONS": settings.DEVICE_ICONS}

def sentry_js(request):
    # Context processor for Sentry JavaScript, in "production".
    val = None
    if settings.DEBUG is False:
        val = settings.SENTRY.get("USER") or None
    return {"SENTRY_JS": val}

def website_title(request):
    # Context processor for website title.
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
