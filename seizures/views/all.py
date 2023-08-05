from django.views.generic import ListView

from ..models import Seizure
from .util import _seize_context


class SeizureAllView(ListView):
    """
    Seizures list all paginated view.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
    model = Seizure
    paginate_by = 10
    template_name = 'seizures.html.djt'

    def get_context_data(self, *args, **kwargs):
        """
        Include context information about seizures and their locations.
        """
        return _seize_context(super().get_context_data(*args, **kwargs))
