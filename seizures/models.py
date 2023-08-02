import json
import urllib

import django.core.validators
from django.db import models
from django.utils import timezone


class Seizure(models.Model):
    """
    Seizure event from the database.
    """

    timestamp = models.DateTimeField(
        primary_key=True,
        editable=True,
        default=timezone.now,
        null=False,
        unique=True,
        help_text='Timestamp of the event'
    )

    device_name = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text='Device Name',
        validators=[django.core.validators.MaxLengthValidator(limit_value=32)]
    )

    device_type = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text='Device Type',
        validators=[django.core.validators.MaxLengthValidator(limit_value=32)]
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text='IP address',
        validators=[django.core.validators.validate_ipv46_address]
    )

    ssid = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text='Optional wireless network SSID name',
        validators=[django.core.validators.MaxLengthValidator(limit_value=32)]
    )

    altitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text='Optional altitude (in feet)',
        validators=[
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    latitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text='GPS Latitude',
        validators=[
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    longitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text='GPS Longitude',
        validators=[
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    address = models.TextField(blank=True, null=True)

    battery = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text='Battery (between 1 and 100)',
        validators=[
            django.core.validators.MinValueValidator(limit_value=1),
            django.core.validators.MaxValueValidator(limit_value=100),
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    brightness = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text = 'Brightness (between 0 and 1)',
        validators=[
            django.core.validators.MinValueValidator(limit_value=0),
            django.core.validators.MaxValueValidator(limit_value=1),
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    volume = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text='Volume (between 0 and 1)',
        validators=[
            django.core.validators.MinValueValidator(limit_value=0),
            django.core.validators.MaxValueValidator(limit_value=1),
            django.core.validators.DecimalValidator(
                max_digits=20,
                decimal_places=15
            )
        ]
    )

    def from_request(self, request):
        """Create seizure object from (JSON POST) request"""

        self.ip_address = self.get_ip_address(request)
        data = json.loads(request.body)

        device = data.get('device')
        self.ssid = self.parse_field(device.get('ssid'))
        self.device_name = self.parse_field(device.get('name'))
        self.device_type = device.get('type')
        self.battery = device.get('battery')
        self.brightness = device.get('brightness')
        self.volume = device.get('volume')

        location = data.get('location')
        self.address = self.parse_field(location.get('address'))
        self.altitude = location.get('altitude')
        self.latitude = location.get('latitude')
        self.longitude = location.get('longitude')

    @staticmethod
    def parse_field(name=None):
        """Parse URL-encoded string values, for database insert"""
        if name is not None and isinstance(name, str):
            return urllib.parse.unquote(name) \
                .replace(u'\xa0', u' ') \
                .replace(u"’", u"'") \
                .replace("\n", ', ')
        return None

    @staticmethod
    def get_ip_address(request):
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            return user_ip.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    class Meta:
        db_table = 'seizures'
        managed = True
        ordering = ['-timestamp']

    def __str__(self):
        return f"<Seizure> {self.device_type} @ {self.timestamp}"

    def __repr__(self):
        return self.__str__()
