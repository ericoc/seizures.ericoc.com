from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from .util import seize_context
from ..models import Seizure


class SeizureRecentView(PermissionRequiredMixin, ListView):
    """
    Seizure list view for the most recent X days.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    since_when = None
    permission_required = 'seizures.view_seizure'
    template_name = 'seizures.html.djt'

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
        return seize_context(super().get_context_data(*args, **kwargs))

    def get_queryset(self, *args, **kwargs):
        """
        Restrict to seizures since a certain time
        """
        return super().get_queryset().filter(
            timestamp__gte=self.since_when
        )
