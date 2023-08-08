from datetime import timedelta

from django.utils import timezone
from django.views.generic import ListView

from ..models import Seizure
from .util import _seize_context


class SeizureRecentView(ListView):
    """
    Seizure paginated list view for the most recent X days.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    since_when = None
    template_name = 'seizures.html.djt'

    def get(self, request, *args, **kwargs):
        """
        Default pagination limit of 10 seizures per page.
        """
        self.paginate_by = request.GET.get('limit', 10) or 10
        return super().get(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        """
        Set the default look-back period to a single day.
        """
        days = 1
        if kwargs.get('days'):
            days = kwargs.get('days')
        delta = timedelta(days=days)
        self.since_when = timezone.now() - delta
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))

    def get_queryset(self, *args, **kwargs):
        """
        Restrict to seizures since a certain time
        """
        return super().get_queryset(*args, **kwargs).filter(
            timestamp__gte=self.since_when
        )
