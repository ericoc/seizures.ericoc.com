# Generated by Django 4.2.3 on 2023-08-03 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seizures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seizure',
            name='address',
            field=models.TextField(blank=True, help_text='Optional address text', null=True),
        ),
    ]
