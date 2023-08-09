import urllib
from django.core.serializers import serialize
from settings import DEVICE_ICONS


def get_ip_address(request):
    """
    Get user IP address from HTTP request.
    """
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        return user_ip.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def parse_field(value=None):
    """
    Parse URL-encoded string values from Apple shortcut, for database insert.
    """
    if value is not None and isinstance(value, str):
        return urllib.parse.unquote(value) \
            .replace(u'\xa0', u' ') \
            .replace(u"’", u"'") \
            .replace("\n", ', ')
    return None


def seize_context(context=None):
    """
    Include serialized seizures and device icons in response context.
    """
    seizures = context.get('seizures')
    if seizures and len(seizures) > 0:
        context['seizures'] = serialize(format='json', queryset=seizures)
        if DEVICE_ICONS:
            context['device_icons'] = DEVICE_ICONS
    return context
