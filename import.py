#!/usr/bin/env python3
"""Import CSV to PostgreSQL."""

import csv
import logging
from datetime import datetime, timezone

import django
django.setup()

from seizures.models import Seizure


logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S %Z', level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(process)d) : %(message)s',
    handlers=[logging.StreamHandler()]
)

# Iterate using CSV DictReader, logging a Seizure database object for each row
with open(file='seizures.csv', mode='r', encoding='utf-8') as fh:

    seizures = []
    for row in csv.DictReader(f=fh):

        seizure = Seizure()
        seizure.timestamp = datetime.fromisoformat(row['timestamp']).replace(
            tzinfo=timezone.utc
        )
        seizure.device_name = row['device_name']
        seizure.device_type = row['device_type']

        seizure.ip_address = row['ip_address']
        if seizure.ip_address == 'NULL':
            seizure.ip_address = None

        seizure.ssid = row['ssid']
        if seizure.ssid == 'NULL':
            seizure.ssid = None

        seizure.battery = row['battery']
        seizure.brightness = row['brightness']
        seizure.volume = row['volume']

        seizure.address = row['address']
        seizure.altitude = row['altitude']
        seizure.latitude = row['latitude']
        seizure.longitude = row['longitude']

        print(seizure)
        print(vars(seizure))

        seizures.append(seizure)

    Seizure.objects.bulk_create(seizures)
    print(len(seizures), 'seizures')
