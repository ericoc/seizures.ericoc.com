from django.conf import settings


def website_title(request):
    """Context processor for website title."""
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
