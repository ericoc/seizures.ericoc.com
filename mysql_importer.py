#!/usr/bin/env python3

"""Import seizures to MySQL from InfluxDB"""

from influxdb import InfluxDBClient

from config import INFLUXDB_CREDS
from database import db_session
from models import Seizure


# Connect to InfluxDB
conn = InfluxDBClient(
    host='127.0.0.1', port=8086, ssl=False, verify_ssl=False,
    username=INFLUXDB_CREDS['username'], password=INFLUXDB_CREDS['password']
)

# Select everything from InfluxDB
results = conn.query(
    f"SELECT * FROM {INFLUXDB_CREDS['measurement']} ORDER BY time ASC",
    database=INFLUXDB_CREDS['database'], epoch='ns'
)
points = results.get_points(measurement=INFLUXDB_CREDS['measurement'])

# Count number in MySQL
sql_seizure_count = Seizure.query.count()
print(f'Count::\t{sql_seizure_count}')

# Delete everything in MySQL
sql_seizure_trunc = Seizure.query.delete()
print(f'Deleted:\t{sql_seizure_trunc}')

# Loop through each InfluxDB point,
#   adding a new MySQL row for each, before committing the transaction
for point in points:
    seizure = Seizure()
    seizure.from_influx(point=point)
    db_session.add(seizure)
db_session.commit()

# Count MySQL again
sql_seizure_count = Seizure.query.count()
print(f'Count:\t{sql_seizure_count}')
