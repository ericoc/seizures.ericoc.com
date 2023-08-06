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
    paginate_by = 10
    since_when = timezone.now() - timedelta(days=1)
    template_name = 'seizures.html.djt'

    def setup(self, request, *args, **kwargs):
        delta = timedelta(days=1)

        if kwargs.get('minutes'):
            delta = timedelta(minutes=kwargs.get('minutes'))

        if kwargs.get('hours'):
            delta = timedelta(hours=kwargs.get('hours'))

        if kwargs.get('days'):
            delta = timedelta(days=kwargs.get('days'))

        if kwargs.get('weeks'):
            delta = timedelta(weeks=kwargs.get('weeks'))

        if kwargs.get('years'):
            delta = timedelta(days=kwargs.get('years')*365)

        self.since_when = timezone.now() - delta
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        context = super().get_context_data(**kwargs)
        context['since_when'] = self.since_when
        return _seize_context(context)

    def get_queryset(self, *args, **kwargs):
        """
        Restrict to seizures since a certain time
        """
        return super().get_queryset(*args, **kwargs).filter(
            timestamp__gte=self.since_when
        )
