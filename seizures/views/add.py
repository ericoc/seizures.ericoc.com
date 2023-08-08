import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ..models import Seizure
from .util import _get_ip_address, _parse_field


class SeizureAddView(View):
    """
    Seizure add view.
    """
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure that the incoming POST is JSON.
        """
        if not request.META.get('CONTENT_TYPE').lower() == 'application/json':
            raise SuspiciousOperation('Invalid content-type.')
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """
        Insert the seizure to the database, using data from the request body.
        """
        data = json.loads(request.body)

        new = Seizure()
        new.ip_address = _get_ip_address(request)

        device = data.get('device')
        new.ssid = _parse_field(value=device.get('ssid'))
        new.device_name = _parse_field(value=device.get('name'))
        new.device_type = device.get('type')
        new.battery = device.get('battery')
        new.brightness = device.get('brightness')
        new.volume = device.get('volume')

        location = data.get('location')
        new.address = _parse_field(value=location.get('address'))
        new.altitude = location.get('altitude')
        new.latitude = location.get('latitude')
        new.longitude = location.get('longitude')

        new.save()

        return HttpResponse(status=201, content='OK', content_type='text/plain')
