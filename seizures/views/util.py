from django.core.serializers import serialize

from settings import GOOGLEMAPS_API_KEY


def _seize_context(context=None):
    """
    Include Google Maps API key, and calculate bounds and center of Google Map,
        based on seizures, for use in the response context.
    """
    seizures = context.get('seizures')
    if seizures and len(seizures) > 0:

        context['googlemaps_api_key'] = GOOGLEMAPS_API_KEY

        latitudes = []
        longitudes = []

        for seizure in seizures:
            latitudes.append(seizure.latitude)
            longitudes.append(seizure.longitude)

        context['center_lat'] = sum(latitudes) / len(latitudes)
        context['center_lng'] = sum(longitudes) / len(longitudes)

        context['min_lat'] = min(latitudes)
        context['min_lng'] = min(longitudes)

        context['max_lat'] = max(latitudes)
        context['max_lng'] = max(longitudes)

        context['seizures'] = serialize('json', seizures)

    return context
