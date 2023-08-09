from django.views.generic import ListView

from ..models import Seizure
from .util import seize_context


class SeizureAllView(ListView):
    """
    Seizures list all paginated view.
    """
    context_object_name = 'seizures'
    date_field = 'timestamp'
    http_method_names = ['get']
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
        return seize_context(super().get_context_data(*args, **kwargs))
