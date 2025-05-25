#!/usr/bin/env python3
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import BaseCommand
from django.utils.translation import ngettext

from ...models import Seizure


class Command(BaseCommand):
    """
    Export all seizure data to SQLite database.
    """
    help = "Export all seizure data to SQLite database."

    def handle(self, *args, **options):

        # Find latest timestamp in SQLite.
        latest = None
        try:
            latest = Seizure.objects.using("sqlite").order_by("-timestamp").\
                first().timestamp
            self.stdout.write(
                self.style.SUCCESS(
                    f"Latest SQLite: {latest.strftime(settings.TIME_FMT)}"
                )
            )

        except (Seizure.DoesNotExist, AttributeError):
            self.stdout.write(self.style.WARNING("Nothing in SQLite!\n"))

        # Gather seizures from Snowflake, based on the latest in SQLite.
        seizures = Seizure.objects
        if latest:
            seizures = seizures.filter(pk__gt=latest)
        seizures = seizures.order_by("timestamp")
        num_seizures = seizures.count()

        # List count of seizures found, and where they are being exported to.
        if num_seizures > 0:
            self.stdout.write(self.style.NOTICE("Exporting %s %s to %s.\n" % (
                    intcomma(num_seizures),
                    ngettext(
                        singular="seizure",
                        plural="seizures",
                        number=num_seizures
                    ),
                    settings.DATABASES["sqlite"]["NAME"]
                )
        ))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "No seizures found for export to %s.\n" % (
                        settings.DATABASES["sqlite"]["NAME"]
                    )
                )
            )

        # Iterate each seizure found.
        for (count, seizure_obj) in enumerate(seizures.all(), start=1):
            seizure_dict = vars(seizure_obj)
            when = seizure_dict.pop("timestamp")
            del seizure_dict["_state"]

            (obj, ctd) = Seizure.objects.using("sqlite").update_or_create(
                timestamp=when,
                defaults=seizure_dict,
                create_defaults=seizure_dict
            )
            if ctd:
                msg = self.style.SUCCESS(f"Created: {obj}\n")
            else:
                msg = self.style.NOTICE(f"Skipping: {obj}\n")
            self.stdout.write(msg)
