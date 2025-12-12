#!/usr/bin/env python3
from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ngettext

from ...models import Seizure


class Command(BaseCommand):
    """
    List, and optionally e-mail, seizures if >=X in past Y hour(s).
    """
    help = "List, and optionally e-mail, seizures if >=X in past Y hour(s)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--hours",
            default=24,
            help="Number of hour(s) to search, previous to now."
                 " (Default: 24)",
            type=int,
        )
        parser.add_argument(
            "--threshold", "-t",
            default=10,
            help="Threshold of # of seizure(s) to search for (>=)."
                 " (Default: 10)",
            type=int,
        )
        parser.add_argument(
            "--email", "-e",
            default=not settings.DEBUG,
            help="Optionally e-mail upon reaching the threshold."
                 f" (Default: {not settings.DEBUG})",
            action="store_true",
        )

    def handle(self, *args, **options):

        # Get the number of hours to search back from now for seizures.
        hours = options.get("hours")

        # Create a datetime of the time however many hours ago.
        since = timezone.localtime() - timedelta(hours=hours)

        # Find and count seizures going back to time requested.
        seizures_objs = Seizure.objects.filter(pk__gte=since)
        num_seizures = seizures_objs.count()

        # List the total number seizures found since when.
        message = (
            f"Found {intcomma(num_seizures)} {ngettext(
                singular="seizure",
                plural="seizures",
                number=num_seizures
            )}, since {naturaltime(since)}"
            f" (on {since.strftime(settings.TIME_FMT)}).\n"
        )

        # Proceed if number of seizures found is >= the threshold given.
        threshold = options.get("threshold")
        if num_seizures >= threshold:

            # Count, and list, the details of when/where/etc. each seizure.
            message += f"\n{settings.CSRF_TRUSTED_ORIGINS[0]}\n"
            for (count, seizure) in enumerate(seizures_objs.all(), start=1):
                message += (
                    f"{count}. {timezone.localtime(value=seizure.pk).strftime(
                        settings.TIME_FMT
                    )} / {seizure.device_type} / "
                    f"{str(seizure.address).replace("\n", ", ")}\n"
                )

            # Consider whether to e-mail.
            do_mail = options.get("email")
            if do_mail:

                # Specify file to record e-mail time, to avoid repeated messages.
                last_mail = Path(Path.home(), f"last_mail_{hours}")
                try:

                    # Get modification time (mtime) of last e-mail file.
                    mailed = timezone.make_aware(
                        datetime.fromtimestamp(last_mail.stat().st_mtime)
                    )

                    # Skip e-mailing if an e-mail was sent within threshold.
                    if mailed >= since:
                        do_mail = False
                        message += "\nSKIPPED threshold e-mail.\nLast e-mail: "
                        message += f"{mailed.strftime(settings.TIME_FMT)}. (>="
                        message += f" {since.strftime(settings.TIME_FMT)}).\n"
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

            else:
                message += "\nSKIPPED threshold e-mail.\n"

        # Finally, show the (on-screen) message!
        self.stdout.write(self.style.SUCCESS(message))
