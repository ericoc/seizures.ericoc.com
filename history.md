# History

This originally began as a single-file Python Flask application, likely some
time in January 2022.

These seizure events have been stored in numerous different databases, having
been migrated at least four (4) times - from MySQL, PostgreSQL, InfluxDB,
Snowflake, and again back to PostgreSQL currently.

In August 2023, I migrated to PostgreSQL (using Django QuerySets), but then
again migrated my Django QuerySets to query a Snowflake warehouse as of
February 2024. After a large, unexpected bill from Snowflake (due to a
cron job), I migrated back to PostgreSQL in early June 2025.
