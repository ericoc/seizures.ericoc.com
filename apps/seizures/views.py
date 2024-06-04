from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.serializers import serialize
from django.utils.timezone import localtime
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from .forms import SeizuresSearchDateForm
from .models import Seizure


class SeizuresView(FormMixin, PermissionRequiredMixin, TemplateView):
    """View seizures between start and end times."""
    dates = initial = {"start": None, "end": None}
    form_class = SeizuresSearchDateForm
    http_method_names = ("get", "post")
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html"

    def setup(self, request, *args, **kwargs):
        """Set default search start and end datetime values."""
        now = localtime()
        self.dates = {"start": now - settings.DEFAULT_SINCE, "end": now}
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        """When valid, use the submitted form search dates."""
        self.dates = form.cleaned_data
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Include device icons, dates, and seizures JSON in context."""
        context = super().get_context_data(**kwargs)
        context["device_icons"] = settings.DEVICE_ICONS

        for date in ("start", "end"):
            context[date] = self.dates[date]

        seizures = Seizure.objects.filter(
            timestamp__gte=self.dates["start"], timestamp__lte=self.dates["end"]
        ).all()
        context["seizures"] = serialize(format="json", queryset=seizures)

        return context

    def get_initial(self):
        """Set initial form search date string values."""
        initial = super().get_initial()
        for date in ("start", "end"):
            initial[date] = self.dates[date].strftime("%Y-%m-%dT%H:%M:%S")
        return initial
