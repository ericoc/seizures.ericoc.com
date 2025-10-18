from django.conf import settings


def device_icons(request):
    # Context processor for device icons.
    return {"DEVICE_ICONS": settings.DEVICE_ICONS}

def website_title(request):
    # Context processor for website title.
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
