#!/usr/bin/env python3
from calendar import day_name
from sys import exit
from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count
from django.db.models.expressions import F

from ...models import Seizure


class Command(BaseCommand):
    """
    Count number of seizures by day of the week.
    """
    help = "Count number of seizures by day of the week."

    def handle(self, *args, **options):

        # Query seizures and count by day of the week.
        seizures_per_dow = Seizure.objects.values(
                weekday=F("timestamp__week_day")
            ).annotate(
                seizures=Count("timestamp__week_day")
            ).order_by("weekday").all()

        # Loop through each day of the week to display number of seizures.
        for item in seizures_per_dow:
            dow_num = item["weekday"]
            dow_name = day_name[dow_num -1]
            seizure_count = item["seizures"]
            self.stdout.write(
                self.style.SUCCESS(
                    f"{item['weekday']}. {dow_name}\t{seizure_count}"
                )
            )

        exit(0)
