# History

This originally began as a single-file Python Flask application, likely some
time in January 2022.

These seizure events have been stored in numerous different databases, having
been migrated at least three (3) times - from MySQL, PostgreSQL, InfluxDB, and
now Snowflake.

In August 2023, I migrated to PostgreSQL (using Django QuerySets), but then
again migrated my Django QuerySets to query a Snowflake warehouse as of
February 2024.
