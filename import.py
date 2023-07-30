#!/usr/bin/env python3
"""Import CSV (from MySQL dump) to PostgreSQL."""

import csv
import logging
import os

from database import db_session
from models import Seizure


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
        db_session.add(seizure)

    # Commit the changes to the database
    db_session.commit()
