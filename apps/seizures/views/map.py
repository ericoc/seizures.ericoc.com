from .base import SeizuresBaseView


class SeizuresMapView(SeizuresBaseView):
    """Leaflet view."""
    days = 1
    template_name = "map.html"
