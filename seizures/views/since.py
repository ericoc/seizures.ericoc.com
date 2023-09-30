from datetime import timedelta

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from seizures.views.util import seize_context
from seizures.models import Seizure


class SeizureSinceView(PermissionRequiredMixin, ListView):
    """
    Seizure list view for the most recent X days.
    """
    allow_empty = True
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    since_delta = settings.DEFAULT_SINCE
    since_when = None
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def setup(self, request, *args, **kwargs):
        """
        Set the look-back timedelta, if requested.
        """

        if kwargs.get("minutes"):
            self.since_delta = timedelta(minutes=kwargs.get("minutes"))

        if kwargs.get("hours"):
            self.since_delta = timedelta(hours=kwargs.get("hours"))

        if kwargs.get("days"):
            self.since_delta = timedelta(days=kwargs.get("days"))

        if kwargs.get("weeks"):
            self.since_delta = timedelta(weeks=kwargs.get("weeks"))

        if kwargs.get("months"):
            self.since_delta = timedelta(days=kwargs.get("months")*30)

        if kwargs.get("years"):
            self.since_delta = timedelta(days=kwargs.get("years")*365)

        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Calculate the look-back datetime using the requested timedelta.
        """
        self.since_when = timezone.now() - self.since_delta
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """
        Filter queryset to seizures recorded since the look-back time.
        """
        return super().get_queryset().filter(timestamp__gte=self.since_when)

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))
