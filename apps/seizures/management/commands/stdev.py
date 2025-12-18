#!/usr/bin/env python3

import csv
from argparse import FileType
from statistics import stdev
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import BaseCommand


'''
SQL query used to generate input CSV file:

SELECT
   DATE_SERIES::DATE AS "date",
   COUNT(seizures.timestamp) AS "count"
FROM
    GENERATE_SERIES(
        (SELECT MIN(DATE(timestamp)) FROM seizures),
        NOW(),
        '1 DAY'::INTERVAL
     ) AS DATE_SERIES
    LEFT JOIN seizures ON seizures.timestamp::DATE = DATE_SERIES::DATE
GROUP BY DATE_SERIES::DATE
ORDER BY DATE_SERIES::DATE;
'''


class Command(BaseCommand):
    """
    Try to find standard deviation of number of seizures per day.
    """
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv", "-c",
            default=None,
            help="csv file with seizure count per day.",
            type=FileType("r"),
            required=True,
        )

    def handle(self, *args, **options):

        seizure_counts = []
        seizure_days = ()
        total_seizures = 0

        for row in csv.DictReader(options.get("csv")):
            num_seizures = int(row.get("count", 0))
            seizure_counts.append(num_seizures)
            seizure_days = seizure_days + (row["date"],)
            total_seizures = total_seizures + num_seizures

        seizure_avg = total_seizures / len(seizure_days)
        seizure_stddev = stdev(seizure_counts)
        self.stdout.write(
            self.style.NOTICE(
                f"{intcomma(total_seizures)} seizures"
                f" across {intcomma(len(seizure_days))} days,"
                f" averaging {intcomma(round(seizure_avg,3))} seizures per day"
                f" with a standard deviation of {round(seizure_stddev,3)}."
            )
        )
