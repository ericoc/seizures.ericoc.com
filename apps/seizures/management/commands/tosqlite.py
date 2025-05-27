#!/usr/bin/env python3
from sys import exit
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

        # Find latest seizure timestamp in SQLite.
        latest = None
        try:
            latest = Seizure.objects.using("sqlite").order_by("-timestamp").\
                first().timestamp
            self.stdout.write(
                self.style.SUCCESS(
                    f"Latest SQLite: {latest.strftime(settings.TIME_FMT)}"
                )
            )

        # Warn if no seizures were found in SQLite.
        except (Seizure.DoesNotExist, AttributeError):
            self.stdout.write(
                self.style.WARNING("Nothing in SQLite!\n")
            )

        # Gather and count seizures from Snowflake, based on latest in SQLite.
        seizures = Seizure.objects
        if latest:
            seizures = seizures.filter(pk__gt=latest)
        seizures = seizures.order_by("timestamp")
        num_seizures = seizures.count()

        # Exit if no seizures were found for export.
        if num_seizures == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "No seizures found for export to"
                    f" {settings.DATABASES['sqlite']['NAME']}."
                )
            )
            exit(0)

        # List count of seizures found, and where they are being exported to.
        self.stdout.write(
            self.style.NOTICE(
                f"Exporting {intcomma(num_seizures)} {ngettext(
                    singular="seizure",
                    plural="seizures",
                    number=num_seizures
                )} to {settings.DATABASES['sqlite']['NAME']}.\n"
            )
        )

        # Iterate each seizure found in Snowflake, for export to SQLite.
        created = 0
        skipped = 0
        for (count, seizure_obj) in enumerate(seizures.all(), start=1):

            # Create a dictionary from Snowflake seizure object.
            seizure_dict = vars(seizure_obj)
            when = seizure_dict.pop("timestamp")
            del seizure_dict["_state"]

            # Create seizure in SQLite, using the Snowflake dictionary.
            (obj, ctd) = Seizure.objects.using("sqlite").update_or_create(
                timestamp=when,
                defaults=seizure_dict,
                create_defaults=seizure_dict
            )

            # Say and count whether each was created in SQLite, or skipped.
            if ctd:
                msg = self.style.SUCCESS(f"Created: {obj}\n")
                created += 1
            else:
                msg = self.style.NOTICE(f"Skipping: {obj}\n")
                skipped += 1
            self.stdout.write(msg)

        # Show final created/skipped, and total.
        self.stdout.write(
            self.style.SUCCESS(
                f"\n{intcomma(created)} created.\n"
                f"{intcomma(skipped)} skipped.\n"
                f"{intcomma(created+skipped)} total.\nDone!"
            )
        )
