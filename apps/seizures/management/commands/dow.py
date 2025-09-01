#!/usr/bin/env python3
from calendar import day_name
from sys import exit
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import BaseCommand

from ...models import Seizure


class Command(BaseCommand):
    """
    Count number of seizures by day of the week.
    """
    help = "Count number of seizures by day of the week."

    def handle(self, *args, **options):
        """Loop through each day of the week, querying seizures for each."""
        for dow_num in range(1, 8):
            dow_name = day_name[dow_num -1]
            dow_count =  Seizure.objects.filter(
                timestamp__week_day=dow_num
            ).count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"{dow_num}. {dow_name}\t{intcomma(dow_count)}"
                )
            )
        exit(0)
