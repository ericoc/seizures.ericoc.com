from django.conf import settings


def device_icons(request):
    # Context processor for device icons.
    return {"DEVICE_ICONS": settings.DEVICE_ICONS}

def time_zone(request):
    # Context processor for time zone name.
    return {"TIME_ZONE": settings.TIME_ZONE}

def website_title(request):
    # Context processor for website title.
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
