#!/usr/bin/env python3
"""import CSV dump from MySQL to PostgreSQL"""

import csv
from datetime import datetime, timezone

# from database import db_session
from models import Seizure


FILENAME = 'seizures.csv'

## example CSV DictReader row contents
# {
#   'timestamp': '2023-07-30 14:30:00',
#   'ssid': 'ericoc',
#   'device': 'pro',
#   'device_type': 'Mac',
#   'ip_address': '2600:dead:beef:de00::1',
#   'latitude': '0.0',
#   'longitude': '0.0',
#   'address': 'Example',
#   'battery': '46',
#   'brightness': '0.834935903549194',
#   'volume': '0.250000000000000',
#   'altitude': '0.000000000000000'
# }
# print(row)

# Open the file using CSV DictReader, creating a Seizure object for each row
with open(FILENAME, 'r') as fh:
    reader = csv.DictReader(fh)
    for row in csv.DictReader(fh):
        seizure = Seizure()
        print(f"{seizure}")

    ## PostgreSQL table structure
    # CREATE TABLE public.seizures (
    #     "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    #     device_name character varying(32)[] NOT NULL,
    #     device_type character varying(32)[] NOT NULL,
    #     ip_address inet NOT NULL,
    #     ssid character varying(32),
    #     location point NOT NULL,
    #     altitude numeric(20,15)
    # );

    ## Commit the changes to the database
    # seizure = Seizure()
    # db_session.add(seizure)
    # db_session.commit()
