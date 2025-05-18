#!/usr/bin/env python3
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ngettext
from pathlib import Path

from ...models import Seizure


class Command(BaseCommand):
    """
    List, and optionally e-mail, seizures if >=X in past Y hour(s).
    """
    help = "List, and optionally e-mail, seizures if >=X in past Y hour(s)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--hours", "-hours", "--hour", "-hour", "--hrs", "-hrs",
            default=24,
            help="Number of hour(s) to search, previous to now. (Default: 24)",
            type=int,
        )
        parser.add_argument(
            "--threshold", "-threshold", "-t", "--t",
            default=15,
            help="Threshold of # of seizure(s) to search for. (Default: 15)",
            type=int,
        )

    def handle(self, *args, **options):

        # Human-readable date format.
        dt_fmt = "%A, %B %d, %Y @ %I:%M:%S %p %Z %z"

        # Get the number of hours to search back from now for seizures.
        hours = options.get("hours")

        # Create a datetime of the time however many hours ago.
        since = timezone.localtime() - timedelta(hours=hours)

        # Find and count seizures going back to time requested.
        seizures_objs = Seizure.objects.filter(pk__gte=since)
        num_seizures = seizures_objs.count()

        # List the total number seizures found since when.
        message = "Found %s %s, since %s (on %s).\n" % (
            intcomma(num_seizures),
            ngettext(
                singular="seizure",
                plural="seizures",
                number=num_seizures
            ),
            naturaltime(since),
            since.strftime(dt_fmt),
        )

        # Proceed if number of seizures found is >= the threshold given.
        threshold = options.get("threshold")
        if num_seizures >= threshold:

            # Count, and list, the details of when/where/etc. each seizure.
            message += "\n"
            for (count, seizure) in enumerate(seizures_objs.all(), start=1):
                message += "%i. %s / %s / %s\n" % (
                    count,
                    timezone.localtime(value=seizure.pk).strftime(dt_fmt),
                    seizure.device_type,
                    str(seizure.address).replace("\n", ", "),
                )

            # Consider whether to e-mail, if DEBUG is False.
            if settings.DEBUG is False:

                # Specify file to record e-mail time, to avoid repeated messages.
                do_mail = False
                last_mail = Path(Path.home(), "last_mail")
                try:

                    # Get modification time (mtime) of last e-mail file.
                    mailed = timezone.make_aware(
                        datetime.fromtimestamp(last_mail.stat().st_mtime)
                    )

                    # Skip e-mailing if an e-mail was sent within threshold.
                    if mailed >= since:
                        message += "\nSKIPPED threshold e-mail.\n"
                        message += f"E-mail sent {mailed.strftime(dt_fmt)}."
                        message += f" (>= {since.strftime(dt_fmt)}).\n"
                    else:
                        do_mail = True

                # Prepare to send e-mail if the file did not exist.
                except FileNotFoundError:
                    do_mail = True

                # Send the e-mail and say so, if it is okay to do so.
                if do_mail is True:
                    if send_mail(
                        subject=f"{settings.WEBSITE_TITLE}: Rescue",
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=(settings.ADMINS[0][1],),
                    ):
                        message += "\nSENT threshold e-mail.\n"

                        # Create file to record time when the e-mail was sent.
                        last_mail.touch()


        # Finally, show the (on-screen) message!
        self.stdout.write(self.style.SUCCESS(message))
