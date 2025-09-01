# Database Queries
---

Some example useful database queries to run.

---
## Average per Day

Divide total number of seizures across unique number of days.

```postgresql
seizures=> SELECT
    TO_CHAR(COUNT(timestamp), 'FM9,999,999') AS "Total Seizures",
    TO_CHAR(COUNT(DISTINCT(DATE(timestamp))), 'FM9,999,999') AS "Total Days",
    COUNT(timestamp) / COUNT(DISTINCT(DATE(timestamp))) AS "Average Seizures per Day"
FROM seizures;
```
```
 Total Seizures | Total Days | Average Seizures per Day
----------------+------------+--------------------------
 11,220         | 1,328      |                        8
(1 row)
```

---
### Device Type

Number of seizures per device type, all time.

```postgresql
seizures=> SELECT
    DEVICE_TYPE AS "Device Type",
    COUNT(DEVICE_TYPE) AS "Count"
FROM seizures
GROUP BY(DEVICE_TYPE)
ORDER BY "Count";
```
```
 Device Type | Count
-------------+-------
 iPad        |     5
 Browser     |    59
 Mac         |   817
 Watch       |  5100
 iPhone      |  5237
(5 rows)
```

---
### Daily

Number of seizures per day, between two dates.

```postgresql
seizures=> SELECT
    date_series::date AS "Date",
    COUNT(seizures.timestamp) AS "Count"
FROM
    generate_series('2025-01-01'::timestamp, '2025-01-15'::timestamp, '1 day'::interval) AS date_series
LEFT JOIN
    seizures ON seizures.timestamp::date = date_series::date
GROUP BY
    date_series
ORDER BY
    date_series;
```
```
    Date    | Count
------------+-------
 2025-01-01 |     0
 2025-01-02 |     0
 2025-01-03 |     3
 2025-01-04 |     3
 2025-01-05 |     7
 2025-01-06 |     4
 2025-01-07 |     6
 2025-01-08 |    11
 2025-01-09 |     5
 2025-01-10 |     3
 2025-01-11 |     4
 2025-01-12 |     0
 2025-01-13 |    12
 2025-01-14 |     5
 2025-01-15 |     8
(15 rows)
```

---
### Timespan

Oldest, and most recent, seizure timestamp all time.

```postgresql
seizures=> SELECT
    TO_CHAR(
        MIN(TIMESTAMP),
        'Day Mon DD YYYY HH12:MI:SS AM TZ OF'
    ) AS "Oldest",
    TO_CHAR(
        MAX(TIMESTAMP),
        'Day Mon DD YYYY HH12:MI:SS AM TZ OF'
    ) AS "Latest"
FROM seizures;
```
```

                  Oldest                   |                  Latest
-------------------------------------------+-------------------------------------------
 Monday    Dec 13 2021 03:02:31 AM UTC +00 | Sunday    Aug 31 2025 04:39:16 PM UTC +00
(1 row)
```

---
### Total

Total number of seizures, over all time.

```postgresql
seizures=> SELECT
    TO_CHAR(
        COUNT(timestamp),
        'FM9,999,999'
    ) AS "Total Seizures"
FROM seizures;
```
```
 Total Seizures
----------------
 11,218
(1 row)
```