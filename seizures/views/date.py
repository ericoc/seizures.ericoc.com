from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.dates import \
    DayArchiveView, MonthArchiveView, YearArchiveView

from ..models import Seizure
from .util import seize_context


class SeizureYearView(PermissionRequiredMixin, YearArchiveView):
    """
    Seizure view for a specific year.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    make_object_list = True
    model = Seizure
    permission_required = 'seizures.view_seizure'
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureMonthView(PermissionRequiredMixin, MonthArchiveView):
    """
    Seizure view for a specific month.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    month_format = '%m'
    permission_required = 'seizures.view_seizure'
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))


class SeizureDayView(PermissionRequiredMixin, DayArchiveView):
    """
    Seizure view for a specific day.
    """
    allow_empty = True
    allow_future = False
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    month_format = '%m'
    permission_required = 'seizures.view_seizure'
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))

