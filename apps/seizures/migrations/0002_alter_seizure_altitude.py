# Generated by Django 5.2.2 on 2025-06-05 01:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seizures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seizure',
            name='altitude',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='Altitude (in meters) where the seizure was recorded.', max_digits=20, null=True, validators=[django.core.validators.DecimalValidator(decimal_places=15, max_digits=20)], verbose_name='Altitude'),
        ),
    ]
