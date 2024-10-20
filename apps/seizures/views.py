from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.utils.timezone import localtime
from django.views.generic import FormView

from .forms import SeizuresSearchDateForm
from .models import Seizure


class SeizuresView(LoginRequiredMixin, FormView):
    """View seizures between start and end times."""
    dates = initial = {"start": None, "end": None}
    form_class = SeizuresSearchDateForm
    http_method_names = ("get", "post")
    model = Seizure
    context_object_name = model.__name__.lower() + "s"
    template_name = "seizures.html"

    def setup(self, request, *args, **kwargs):
        # Set default search start and end datetime values.
        now = localtime()
        self.dates = {"start": now - settings.DEFAULT_SINCE, "end": now}
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        # When valid, use the submitted form search dates.
        self.dates = form.cleaned_data
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        # Include device icons, dates, and seizures JSON in context.
        context = super().get_context_data(**kwargs)

        for date in "start", "end":
            context[date] = self.dates[date]

        context[self.context_object_name] = serialize(
            format="json",
            queryset=self.model.objects.filter(
                timestamp__gte=self.dates["start"],
                timestamp__lte=self.dates["end"]
            ).all()
        )
        return context

    def get_initial(self):
        # Set initial form search date string values.
        initial = super().get_initial()
        for when in "start", "end":
            initial[when] = self.dates[when].strftime("%Y-%m-%dT%H:%M")
        return initial


class TableView(SeizuresView):
    template_name = "table.html"
