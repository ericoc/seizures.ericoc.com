from django.db import models
from django.core.validators import (
    DecimalValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
)
from django.utils.timezone import now, localtime


class Seizure(models.Model):
    """Seizure."""
    timestamp = models.DateTimeField(
        primary_key=True,
        default=now,
        null=False,
        unique=True,
        help_text="Timestamp of the seizure.",
        verbose_name="Timestamp"
    )
    device_name = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text="Name of device used to record the seizure.",
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name="Device Name"
    )
    device_type = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text="Type of device used to record the seizure",
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name="Device Type"
    )
    ssid = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Wireless network SSID detected upon seizure recording.",
        validators=(MaxLengthValidator(limit_value=32),),
        verbose_name="Network SSID"
    )
    altitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text="Altitude (in feet) where the seizure was recorded.",
        validators=(DecimalValidator(max_digits=20, decimal_places=15),),
        verbose_name="Altitude"
    )
    latitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text="GPS latitude where the seizure was recorded.",
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=90),
            MinValueValidator(limit_value=-90)
        ),
        verbose_name="GPS Latitude"
    )
    longitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        help_text="GPS longitude where the seizure was recorded.",
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=180),
            MinValueValidator(limit_value=-180)
        ),
        verbose_name="GPS Longitude"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Address where the seizure was recorded.",
        verbose_name="Address"
    )
    battery = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text="Device battery (between 1 and 100) upon seizure recording.",
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=100),
            MinValueValidator(limit_value=1)
        ),
        verbose_name="Device Battery"
    )
    brightness = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text="Device brightness (between 0 and 1) upon seizure recording.",
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=1),
            MinValueValidator(limit_value=0)
        ),
        verbose_name="Device Brightness"
    )
    volume = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        blank=True,
        null=True,
        help_text="Device volume (between 0 and 1) upon seizure recording.",
        validators=(
            DecimalValidator(max_digits=20, decimal_places=15),
            MaxValueValidator(limit_value=1),
            MinValueValidator(limit_value=0)
        ),
        verbose_name="Volume"
    )

    class Meta:
        db_table = "seizures"
        managed = True
        ordering = ("-timestamp",)
        required_db_vendor = "snowflake"
        verbose_name = "Seizure"
        verbose_name_plural = "Seizures"

    def __repr__(self):
        return "%s: %s" % (
            self.__class__.__name__,
            self.__str__()
        )

    def __str__(self):
        _fmt = "%A, %B %d %Y @ %I:%M:%S %p %Z"
        return "%s (%s)" % (
            localtime(self.timestamp).strftime(_fmt),
            self.device_type
        )
