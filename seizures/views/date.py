from django.views.generic.dates import \
    DayArchiveView, MonthArchiveView, YearArchiveView

from ..models import Seizure
from .util import _seize_context


class SeizureYearView(YearArchiveView):
    """
    Seizure paginated view for a specific year.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    make_object_list = True
    model = Seizure
    template_name = 'seizures.html.djt'

    def get(self, request, *args, **kwargs):
        """
        Default pagination limit of 10 seizures per page.
        """
        self.paginate_by = request.GET.get('limit', 10) or 10
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))


class SeizureMonthView(MonthArchiveView):
    """
    Seizure paginated view for a specific month.
    """
    allow_empty = True
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    month_format = '%m'
    template_name = 'seizures.html.djt'

    def get(self, request, *args, **kwargs):
        """
        Default pagination limit of 10 seizures per page.
        """
        self.paginate_by = request.GET.get('limit', 10) or 10
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))


class SeizureDayView(DayArchiveView):
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
    template_name = 'seizures.html.djt'

    def get(self, request, *args, **kwargs):
        """
        Default pagination limit of 10 seizures per page.
        """
        self.paginate_by = request.GET.get('limit', 10) or 10
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))

