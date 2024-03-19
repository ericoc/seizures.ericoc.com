from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.core.serializers import serialize
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime, make_aware
from django.views.generic import ListView

from .forms import SeizuresSearchDateForm
from .models import Seizure


class SeizuresView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """View seizures between start and end times."""
    allow_empty = True
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get", "post")
    model = Seizure
    permission_required = "seizures.view_seizure"
    search_form = SeizuresSearchDateForm()
    search_dates = {"start": None, "end": None}
    template_name = "seizures.html"

    def dispatch(self, request, *args, **kwargs):
        """Set default search start and end datetime values."""

        # Default current end time is the current local time.
        if not self.search_dates["end"]:
            self.search_dates["end"] = localtime()

        # Default start time is 24 hours before the end time.
        if not self.search_dates["start"]:
            self.search_dates["start"] = (
                    self.search_dates["end"] - settings.DEFAULT_SINCE
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter seizures recorded between datetime values."""
        return super().get_queryset().filter(
            timestamp__gte=self.search_dates["start"],
            timestamp__lte=self.search_dates["end"]
        )

    def post(self, request, *args, **kwargs):
        """Handle date search form POST requests."""
        self.search_form = SeizuresSearchDateForm(request.POST)
        if self.search_form.is_valid():
            for i in ['start', 'end']:
                parsed = make_aware(parse_datetime(request.POST.get(i)))
                self.search_dates[i] = parsed
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Include icons, search times, and serialized items in context."""
        context = super().get_context_data(*args, **kwargs)

        context["device_icons"] = settings.DEVICE_ICONS
        context["start"] = self.search_dates["start"]
        context["end"] = self.search_dates["end"]

        # Format search times as text, and fill initial form values.
        _initial = {}
        for i in ['start', 'end']:
            _initial[i] = self.search_dates[i].strftime("%Y-%m-%dT%H:%M:%S")
        self.search_form.initial = _initial
        context["search_form"] = self.search_form

        # Serialize to JSON, for JavaScript inclusion.
        obj = context.get(self.context_object_name)
        if obj:
            context[self.context_object_name] = serialize(
                format="json",
                queryset=obj
            )

        return context
