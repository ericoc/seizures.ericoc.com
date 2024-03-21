from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.serializers import serialize
from django.utils.timezone import localtime
from django.views.generic import FormView

from .forms import SeizuresSearchDateForm
from .models import Seizure


class SeizuresView(PermissionRequiredMixin, FormView):
    """View seizures between start and end times."""
    dates = initial = {}
    form_class = SeizuresSearchDateForm
    http_method_names = ("get", "post")
    permission_required = "seizures.view_seizure"
    seizures = None
    template_name = "seizures.html"

    def setup(self, request, *args, **kwargs):
        """Set default search start and end datetime values."""
        self.dates["end"] = localtime()
        self.dates["start"] = self.dates["end"] - settings.DEFAULT_SINCE
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        """When valid, use the submitted form search dates."""
        self.dates = form.cleaned_data
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Include icons, search datetimes, and seizures JSON in context."""
        context = super().get_context_data(**kwargs)
        context["device_icons"] = settings.DEVICE_ICONS
        context["start"] = self.dates["start"]
        context["end"] = self.dates["end"]
        context["seizures"] = serialize(
            format="json",
            queryset=Seizure.objects.filter(
                timestamp__gte=self.dates["start"],
                timestamp__lte=self.dates["end"]
            ).all()
        )
        return context

    def get_initial(self):
        """Fill in search form date inputs with correctly formatted strings."""
        initial = super().get_initial()
        for date in ("start", "end"):
            initial[date] = initial[date].strftime("%Y-%m-%dT%H:%M:%S")
        return initial
