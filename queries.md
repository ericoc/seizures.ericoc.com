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
    generate_series('2024-12-15'::date, '2025-01-03'::date, '1 day'::interval) AS date_series
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
 2024-12-15 |     6
 2024-12-16 |     4
 2024-12-17 |     1
 2024-12-18 |     2
 2024-12-19 |     0
 2024-12-20 |     0
 2024-12-21 |     3
 2024-12-22 |     2
 2024-12-23 |     1
 2024-12-24 |     0
 2024-12-25 |     1
 2024-12-26 |     2
 2024-12-27 |     0
 2024-12-28 |     2
 2024-12-29 |     0
 2024-12-30 |     0
 2024-12-31 |     0
 2025-01-01 |     0
 2025-01-02 |     2
 2025-01-03 |     2
(20 rows)
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
