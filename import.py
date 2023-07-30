#!/usr/bin/env python3
"""Import CSV (from MySQL dump) to PostgreSQL."""

import csv
import logging
import os

# from database import db_session
from models import Seizure


## PostgreSQL table
# CREATE TABLE public.seizures (
#   "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
#   device_name character varying(32)[] NOT NULL,
#   device_type character varying(32)[] NOT NULL,
#   ip_address inet NOT NULL,
#   ssid character varying(32),
#   location point NOT NULL,
#   altitude numeric(20,15)
# );

## CSV DictReader row example
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

# Logging
LOG_LEVEL = logging.INFO
if os.environ.get('SEIZURE_DEBUG'):
    LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S %Z', level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] (%(process)d) : %(message)s',
    handlers=[logging.StreamHandler()]
)

FILENAME = os.environ.get('SEIZURE_FILENAME') or 'seizures.csv'
logging.info('CSV: %s', FILENAME)

# Iterate using CSV DictReader, logging a Seizure database object for each row
with open(file=FILENAME, mode='r', encoding='utf-8') as fh:
    logging.debug(fh)
    for row in csv.DictReader(f=fh):
        logging.debug(row)
        seizure = Seizure()
        seizure.from_row(row=row)
        logging.info(seizure)
        logging.debug(vars(seizure))
        # Commit the changes to the database
        # db_session.add(seizure)
        # db_session.commit()
