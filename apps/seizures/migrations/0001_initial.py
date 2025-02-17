# Generated by Django 5.1.2 on 2024-10-18 19:54

import django.core.validators
import django.utils.timezone
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seizure',
            fields=[
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp of the seizure.', primary_key=True, serialize=False, unique=True, verbose_name='Timestamp')),
                ('device_name', models.CharField(help_text='Name of device used to record the seizure.', max_length=32, validators=[django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Device Name')),
                ('device_type', models.CharField(help_text='Type of device used to record the seizure', max_length=32, validators=[django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Device Type')),
                ('ssid', models.CharField(blank=True, help_text='Wireless network SSID detected upon seizure recording.', max_length=32, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=32)], verbose_name='Network SSID')),
                ('altitude', models.DecimalField(blank=True, decimal_places=15, help_text='Altitude (in feet) where the seizure was recorded.', max_digits=20, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20)], verbose_name='Altitude')),
                ('latitude', models.DecimalField(decimal_places=15, help_text='GPS latitude where the seizure was recorded.', max_digits=20, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20), django.core.validators.MaxValueValidator(limit_value=Decimal('90')), django.core.validators.MinValueValidator(limit_value=Decimal('-90'))], verbose_name='GPS Latitude')),
                ('longitude', models.DecimalField(decimal_places=15, help_text='GPS longitude where the seizure was recorded.', max_digits=20, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20), django.core.validators.MaxValueValidator(limit_value=Decimal('180')), django.core.validators.MinValueValidator(limit_value=Decimal('-180'))], verbose_name='GPS Longitude')),
                ('address', models.TextField(blank=True, help_text='Address where the seizure was recorded.', null=True, verbose_name='Address')),
                ('battery', models.DecimalField(blank=True, decimal_places=15, help_text='Device battery (between 1 and 100) upon seizure recording.', max_digits=20, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20), django.core.validators.MaxValueValidator(limit_value=Decimal('100')), django.core.validators.MinValueValidator(limit_value=Decimal('1'))], verbose_name='Device Battery')),
                ('brightness', models.DecimalField(blank=True, decimal_places=15, help_text='Device brightness (between 0 and 1) upon seizure recording.', max_digits=20, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20), django.core.validators.MaxValueValidator(limit_value=Decimal('1')), django.core.validators.MinValueValidator(limit_value=Decimal('0'))], verbose_name='Device Brightness')),
                ('volume', models.DecimalField(blank=True, decimal_places=15, help_text='Device volume (between 0 and 1) upon seizure recording.', max_digits=20, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20), django.core.validators.MaxValueValidator(limit_value=Decimal('1')), django.core.validators.MinValueValidator(limit_value=Decimal('0'))], verbose_name='Volume')),
            ],
            options={
                'verbose_name': 'Seizure',
                'verbose_name_plural': 'Seizures',
                'db_table': 'seizures',
                'ordering': ('-timestamp',),
                'get_latest_by': ('-timestamp',),
                'managed': True,
                'required_db_vendor': 'snowflake',
            },
        ),
    ]
