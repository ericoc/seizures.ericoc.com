from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from seizures.models import Seizure
from seizures.views.util import seize_context


class SeizureAllView(PermissionRequiredMixin, ListView):
    """
    Seizures list all view.
    """
    context_object_name = "seizures"
    date_field = "timestamp"
    http_method_names = ("get",)
    model = Seizure
    permission_required = "seizures.view_seizure"
    template_name = "seizures.html.djt"

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return seize_context(super().get_context_data(*args, **kwargs))
