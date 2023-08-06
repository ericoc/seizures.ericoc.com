from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ..models import Seizure


class SeizureAddView(View):
    """
    Seizure add view.
    """
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):

        if not request.META.get('CONTENT_TYPE').lower() == 'application/json':
            raise SuspiciousOperation('Invalid content-type.')

        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        seizure = Seizure()
        seizure.from_request(request)
        seizure.save()

        return HttpResponse(status=201, content='OK', content_type='text/plain')
