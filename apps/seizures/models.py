from decimal import Decimal

from django.db import models
from django.core.validators import (
    DecimalValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
)
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Seizure(models.Model):
    """Seizure."""
    timestamp = models.DateTimeField(
        primary_key=True,
        default=now,
        null=False,
        unique=True,
        help_text=_("Timestamp of the seizure."),
        verbose_name=_("Timestamp")
    )
    device_name = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text=_("Name of device used to record the seizure."),
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name=_("Device Name")
    )
    device_type = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text=_("Type of device used to record the seizure"),
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name=_("Device Type")
    )
    ssid = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text=_("Wireless network SSID detected upon seizure recording."),
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name=_("Network SSID")
    )
    altitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text=_("Altitude (in meters) where the seizure was recorded."),
        validators=(DecimalValidator(max_digits=20, decimal_places=15),),
        verbose_name=_("Altitude")
    )
    latitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text=_("GPS latitude where the seizure was recorded."),
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=Decimal(90)),
            MinValueValidator(limit_value=Decimal(-90))
        ),
        verbose_name=_("GPS Latitude")
    )
    longitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text=_("GPS longitude where the seizure was recorded."),
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=Decimal(180)),
            MinValueValidator(limit_value=Decimal(-180))
        ),
        verbose_name=_("GPS Longitude")
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text=_("Address where the seizure was recorded."),
        verbose_name=_("Address")
    )
    battery = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text=_(
            "Device battery (between 1 and 100) upon seizure recording."
        ),
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=Decimal(100)),
            MinValueValidator(limit_value=Decimal(1))
        ),
        verbose_name=_("Device Battery")
    )
    brightness = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text=_(
            "Device brightness (between 0 and 1) upon seizure recording."
        ),
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=Decimal(1)),
            MinValueValidator(limit_value=Decimal(0))
        ),
        verbose_name=_("Device Brightness")
    )
    volume = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text=_("Device volume (between 0 and 1) upon seizure recording."),
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=Decimal(1)),
            MinValueValidator(limit_value=Decimal(0))
        ),
        verbose_name=_("Volume")
    )

    class Meta:
        db_table = "seizures"
        managed = True
        get_latest_by = ordering = ("-timestamp",)
        verbose_name = _("Seizure")
        verbose_name_plural = _("Seizures")

    def __iter__(self):
        return self

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self):
        return f"{self.timestamp} ({self.device_type})"
