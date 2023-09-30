from django.conf import settings
from django.core.serializers import serialize


def seize_context(context=None):
    """
    Include serialized seizures and device icons in response context.
    """
    seizures = context.get("seizures")
    if seizures:
        context["seizures"] = serialize(format="json", queryset=seizures)
        if settings.DEVICE_ICONS:
            context["device_icons"] = settings.DEVICE_ICONS
    return context
