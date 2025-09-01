from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.utils.timezone import localtime
from django.views.generic import FormView, RedirectView

from .forms import SeizuresSearchDateForm
from .models import Seizure


class SeizuresBaseView(LoginRequiredMixin, FormView):
    """Base view for searching seizures between start and end times."""
    dates = initial = {"start": None, "end": None}
    days = 0
    form_class = SeizuresSearchDateForm
    http_method_names = ("get", "post")
    model = Seizure

    def setup(self, request, *args, **kwargs):
        # Set search start/end datetime values.
        if self.days:
            now = localtime()
            self.dates = {
                "start": now - timedelta(days=self.days),
                "end": now
            }
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        # Use valid submitted form search dates.
        self.dates = form.cleaned_data
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        # Include search dates, and any seizures JSON, in context.
        context = super().get_context_data(**kwargs)
        context["start"] = self.dates["start"]
        context["end"] = self.dates["end"]
        if self.days:
            context["seizures"] = serialize(
                format="json",
                queryset=self.model.objects.filter(
                    timestamp__gte=context["start"],
                    timestamp__lte=context["end"]
                ).all()
            )
        return context

    def get_initial(self):
        # Determine and set initial form search date string values.
        initial = super().get_initial()
        for when in ("start", "end"):
            dt = self.dates.get(when)
            if dt:
                initial[when] = dt.strftime("%Y-%m-%dT%H:%M")
        return initial


class SeizuresMainView(RedirectView):
    """Main view redirects to map."""
    pattern_name = "map"


class SeizuresMapView(SeizuresBaseView):
    """Leaflet view."""
    days = 1
    template_name = "map.html"


class SeizuresChartView(SeizuresBaseView):
    """Highcharts view."""
    days = 365
    template_name = "chart.html"

    # TODO: update SeizuresChartView to use a query more like this, in order
    #   to chart days with zero (0) seizures, per GitHub issue #3:
    #   https://github.com/ericoc/seizures.ericoc.com/issues/3


class SeizuresTableView(SeizuresBaseView):
    """DataTables view."""
    days = 90
    template_name = "table.html"
