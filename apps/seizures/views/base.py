from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.serializers import serialize
from django.views.generic import ListView

from .forms import SeizuresSearchDateForm
from ..models import Seizure


class SeizuresBaseView(PermissionRequiredMixin, ListView):
    """Seizures base view."""
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html"

    def get_context_data(self, *args, **kwargs):
        """Include search form, and JSON seizure data, in response context."""
        context = super().get_context_data(*args, **kwargs)
        context["device_icons"] = settings.DEVICE_ICONS
        context["search_form"] = SeizuresSearchDateForm()
        seizures = context.get("seizures")
        if seizures:
            context["seizures"] = serialize(format="json", queryset=seizures)
        return context
