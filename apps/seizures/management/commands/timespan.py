#!/usr/bin/env python3
from sys import exit
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime, timedelta
from django.utils.translation import ngettext

from ...models import Seizure


class Command(BaseCommand):
    """
    Count number of seizures per day.
    """
    help = "Count number of seizures per day."

    def add_arguments(self, parser):
        """Allow setting previous number of days to search for seizures."""
        parser.add_argument(
            "--days", "--day", "-day", "-days", "-d", "--d",
            default=1,
            help="Days (Default: 1)",
            type=int,
        )

    def handle(self, *args, **options):
        """Count number of seizures, per day, since the number of days."""
        days = options.get("days")
        if days:
            when = localtime() - timedelta(days=days)
            seizures_objs = Seizure.objects.filter(pk__gte=when)
            num_seizures = seizures_objs.count()

            # Exit OK if no seizures found.
            if not num_seizures:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"No seizures found since {naturaltime(when)}"
                        f" on {when.strftime(settings.TIME_FMT)}."
                    )
                )
                exit(1)

            # List number of seizures found.
            message = (
                f"Found {intcomma(num_seizures)}"
                f" {ngettext(
                    singular="seizure", plural="seizures",
                    number=num_seizures
                )}"
                f" since {naturaltime(when)}"
                f" on {when.strftime(settings.TIME_FMT)}.\n"
            )
            self.stdout.write(self.style.SUCCESS(message))
            exit(0)
