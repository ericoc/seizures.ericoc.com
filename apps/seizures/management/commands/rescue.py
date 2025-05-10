#!/usr/bin/env python3
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime, timedelta
from django.utils.translation import ngettext

from ...models import Seizure


# Date/time format.
DT_FMT = "%A, %B %d, %Y @ %I:%M:%S %p %Z %z"


class Command(BaseCommand):
    """
    List seizures if there are more than X in the past Y hours.
    """
    help = "List seizures if there are more than X in the past Y hours."

    def add_arguments(self, parser):
        parser.add_argument(
            "--hours", "-hours", "--hour", "-hour", "--hrs", "-hrs",
            default=1,
            help="Number of hour(s) to search, previous to now. (Default: 24)",
            type=int,
        )
        parser.add_argument(
            "--threshold", "-threshold", "-t", "--t",
            default=15,
            help="Threshold of # of seizures to search for. (Default: 15)",
            type=int,
        )

    def handle(self, *args, **options):
        """Count recent seizures."""
        hours = options.get("hours")
        since = localtime() - timedelta(hours=hours)
        threshold = options.get("threshold")
        seizures_objs = Seizure.objects.filter(pk__gte=since)
        num_seizures = seizures_objs.count()

        if num_seizures >= threshold:
            message = "Found %s %s since %s on %s.\n" % (
                intcomma(num_seizures),
                ngettext(
                singular="seizure",
                    plural="seizures",
                    number=num_seizures
                ),
                naturaltime(since),
                since.strftime(DT_FMT),
            )
            for (count, seizure) in enumerate(seizures_objs.all(), start=1):
                message += "%i. %s / %s / %s\n" % (
                    count,
                    seizure.device_type,
                    localtime(value=seizure.pk).strftime(DT_FMT),
                    str(seizure.address).replace("\n", ", "),
                )
            self.stdout.write(self.style.SUCCESS(message))
