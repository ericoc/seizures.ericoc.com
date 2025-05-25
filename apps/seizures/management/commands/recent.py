#!/usr/bin/env python3
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime, timedelta
from django.utils.translation import ngettext
from sys import exit

from ...models import Seizure


class Command(BaseCommand):
    """
    Recent seizures.
    """
    help = "Count recent seizures, with e-mail alert threshold."

    def add_arguments(self, parser):
        """Allow setting time to search for recent seizures, and threshold."""
        parser.add_argument(
            "--threshold", "-threshold", "-t", "--t",
            help="Send an e-mail upon this threshold of seizures.",
            type=int,
        )
        since_group = parser.add_argument_group(
            title="since",
            description="Search seizures since when? (default: 1 Day)",
        )
        since_group.add_argument(
            "--hours", "--hour", "-hr", "-hrs", "--hr", "--hrs",
            help="Hours",
            type=int,
        )
        since_group.add_argument(
            "--weeks", "--week", "-week", "-weeks", "-w", "--w", "-wks", "--wks",
            help="Weeks",
            type=int,
        )
        since_group.add_argument(
            "--days", "--day", "-day", "-days", "-d", "--d",
            default=1,
            help="Days (Default: 1)",
            type=int,
        )

    def handle(self, *args, **options):
        """Count recent seizures."""

        # Find whatever time range has been chosen, finally defaulting to days.
        for time_type in ("hours", "weeks", "days"):
            time_value = options.get(time_type)

            # Query for seizures during the time range.
            if time_value:
                when = localtime() - timedelta(**{time_type: time_value})
                seizures_objs = Seizure.objects.filter(pk__gte=when)
                num_seizures = seizures_objs.count()

                # Exit OK if no seizures found.
                if not num_seizures:
                    self.stdout.write(
                        self.style.SUCCESS(
                            "No seizures found since %s on %s." % (
                                naturaltime(when),
                                when.strftime(settings.TIME_FMT),
                            )
                        )
                    )
                    exit(0)

                # List number of seizures found.
                message = "Found %s %s since %s on %s.\n" % (
                    intcomma(num_seizures),
                    ngettext(
                        singular="seizure",
                        plural="seizures",
                        number=num_seizures
                    ),
                    naturaltime(when),
                    when.strftime(settings.TIME_FMT),
                )

                # List each seizure found, when necessary.
                threshold = options.get("threshold")
                verbosity = options.get("verbosity")
                if verbosity or threshold is not None:
                    message += "---\n"
                    i = 0
                    for seizure_obj in seizures_objs.all():
                        i = i + 1
                        message += "%i. %s / %s / %s\n" % (
                            i,
                            seizure_obj.device_type,
                            localtime(value=seizure_obj.pk).strftime(
                                settings.TIME_FMT
                            ),
                            str(seizure_obj.address).replace("\n", ", "),
                        )

                    # Say so if the threshold was reached, and send e-mail.
                    if threshold and num_seizures >= threshold:
                        message += "---\n"
                        message += "Threshold reached (%i >= %i)!\n" % (
                            num_seizures,
                            threshold
                        )
                        if send_mail(
                            subject=settings.WEBSITE_TITLE,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=(settings.ADMINS[0][1],),
                        ):
                            self.stdout.write(self.style.SUCCESS(message))
                            message += "Threshold e-mail alert message sent.\n"

                #
                self.stdout.write(self.style.SUCCESS(message))
                exit(0)
