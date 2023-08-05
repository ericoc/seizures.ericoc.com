from datetime import timedelta

from django.utils import timezone
from django.views.generic import ListView

from ..models import Seizure
from .util import _seize_context


class SeizureRecentView(ListView):
    """
    Seizure paginated list view for the most recent 24 hours.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))

    def get_queryset(self, *args, **kwargs):
        """
        Get seizures from the past 24 hours.
        """
        return super().get_queryset(*args, **kwargs).filter(
            timestamp__gte=timezone.now() - timedelta(days=1)
        )
