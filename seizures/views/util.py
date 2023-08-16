from django.core.serializers import serialize

from settings import DEVICE_ICONS


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
