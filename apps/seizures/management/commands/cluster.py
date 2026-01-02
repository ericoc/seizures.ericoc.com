#!/usr/bin/env python3

from datetime import datetime
from pytz import timezone
from sys import exit
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime


from ...models import Seizure


class Command(BaseCommand):
    """
    Count number of seizures by day of the week, over all time.
    """
    help = "Count number of seizures by day of the week, over all time."

    def handle(self, *args, **options):

        # Get all seizures since I broke my collarbone.
        collarbone = localtime(
            datetime(
                year=2025, month=9, day=8, hour=0, minute=0, second=0,
                tzinfo=timezone(settings.TIME_ZONE)
            )
        )
        all_seizures = Seizure.objects.filter(timestamp__gte=collarbone)

        # Iterate each of the past seizures.
        each_seizure = all_seizures.all()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{intcomma(all_seizures.count())} seizures"
                f"\tsince {collarbone.strftime(settings.TIME_FMT)}"
            )
        )

        past_timestamp = None
        for i, seizure in enumerate(each_seizure, start=0):

            # Localize and format the timestamp.
            seizure_timestamp = localtime(seizure.timestamp)
            seizure_time_fmt = seizure_timestamp.strftime(settings.TIME_FMT)

            out_msg = f"{i}.\t{seizure_time_fmt}\t"
            style_msg = self.style.SUCCESS(out_msg)

            # Compare the seizure timestamp...
            if past_timestamp:
                past_diff = past_timestamp - seizure_timestamp
                past_diff_seconds = past_diff.seconds

                # Style seizures that occurred approx. ten (~10) minutes apart.
                if past_diff_seconds <= 1260:
                    out_msg += f"{intcomma(round(past_diff.seconds/60, 1))} min. before next"
                    style_msg = self.style.ERROR(out_msg)

                # Style seizures that occurred nearly one (1) hour apart.
                elif past_diff_seconds >= 3300 and past_diff_seconds <= 3900:
                    out_msg += f"{intcomma(round(past_diff.seconds/60/60, 1))} hour before next"
                    style_msg = self.style.WARNING(out_msg)

                # Style seizures that occurred nearly two (2) hours apart.
                elif past_diff_seconds >= 6800 and past_diff_seconds <= 7600:
                    out_msg += f"{intcomma(round(past_diff.seconds/60/60, 1))} hours before next"
                    style_msg = self.style.WARNING(out_msg)

                # Style seizures that occurred nearly three (3) hours apart.
                elif past_diff_seconds >= 10444 and past_diff_seconds <= 11160:
                    out_msg += f"{intcomma(round(past_diff.seconds/60/60, 1))} hours before next"
                    style_msg = self.style.WARNING(out_msg)


                # List the styled seizure message.
                self.stdout.write(style_msg)

            past_timestamp = seizure_timestamp

        exit(0)
