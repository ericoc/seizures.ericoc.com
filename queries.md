# Database Queries

Example useful database queries to run, assuming `America/New_York` time zone,
set with the following:

```
seizures=> SET SESSION TIME ZONE 'America/New_York';
SET
```

---

## Average per Day

Divide total number of seizures across unique number of days.

```sql
seizures=> SELECT
    TO_CHAR(COUNT(timestamp), 'FM9,999,999') AS "Total Seizures",
    TO_CHAR(COUNT(DISTINCT(DATE(timestamp))), 'FM9,999,999') AS "Total Days",
    COUNT(timestamp) / COUNT(DISTINCT(DATE(timestamp))) AS "Average Seizures per Day"
FROM seizures;

 Total Seizures | Total Days | Average Seizures per Day
----------------+------------+--------------------------
 11,246         | 1,335      |                        8
(1 row)
```

## Device Type

Number of seizures per device type, over all time.

```sql
seizures=> SELECT
    DEVICE_TYPE AS "Device Type",
    COUNT(DEVICE_TYPE) AS "Count"
FROM seizures
GROUP BY(DEVICE_TYPE)
ORDER BY "Count";

 Device Type | Count
-------------+-------
 iPad        |     5
 Browser     |    59
 Mac         |   817
 Watch       |  5116
 iPhone      |  5249
(5 rows)
```

## Time

Number of seizures over time, including days with zero (0) seizures, for issue #3.

### Dates

Number of seizures per day, between two (2) specific dates.

```sql
seizures=> SELECT
   TO_CHAR(DATE_SERIES::DATE, 'Dy Mon DD YYYY HH12:MI:SS AM TZ OF') AS "Date",
   COUNT(seizures.timestamp) AS "Count"
FROM
    GENERATE_SERIES(
        '2024-12-15',
        '2025-01-15',
        '1 DAY'::INTERVAL
     ) AS DATE_SERIES
    LEFT JOIN seizures ON seizures.timestamp::DATE = DATE_SERIES::DATE
GROUP BY DATE_SERIES::DATE ORDER BY DATE_SERIES::DATE;

                Date                 | Count
-------------------------------------+-------
 Sun Dec 15 2024 12:00:00 AM EST -05 |     6
 Mon Dec 16 2024 12:00:00 AM EST -05 |     4
 Tue Dec 17 2024 12:00:00 AM EST -05 |     1
 Wed Dec 18 2024 12:00:00 AM EST -05 |     2
 Thu Dec 19 2024 12:00:00 AM EST -05 |     0
 Fri Dec 20 2024 12:00:00 AM EST -05 |     0
 Sat Dec 21 2024 12:00:00 AM EST -05 |     3
 Sun Dec 22 2024 12:00:00 AM EST -05 |     2
 Mon Dec 23 2024 12:00:00 AM EST -05 |     1
 Tue Dec 24 2024 12:00:00 AM EST -05 |     0
 Wed Dec 25 2024 12:00:00 AM EST -05 |     1
 Thu Dec 26 2024 12:00:00 AM EST -05 |     2
 Fri Dec 27 2024 12:00:00 AM EST -05 |     0
 Sat Dec 28 2024 12:00:00 AM EST -05 |     2
 Sun Dec 29 2024 12:00:00 AM EST -05 |     0
 Mon Dec 30 2024 12:00:00 AM EST -05 |     0
 Tue Dec 31 2024 12:00:00 AM EST -05 |     0
 Wed Jan 01 2025 12:00:00 AM EST -05 |     0
 Thu Jan 02 2025 12:00:00 AM EST -05 |     2
 Fri Jan 03 2025 12:00:00 AM EST -05 |     2
 Sat Jan 04 2025 12:00:00 AM EST -05 |     7
 Sun Jan 05 2025 12:00:00 AM EST -05 |     3
 Mon Jan 06 2025 12:00:00 AM EST -05 |     7
 Tue Jan 07 2025 12:00:00 AM EST -05 |     2
 Wed Jan 08 2025 12:00:00 AM EST -05 |    12
 Thu Jan 09 2025 12:00:00 AM EST -05 |     4
 Fri Jan 10 2025 12:00:00 AM EST -05 |     3
 Sat Jan 11 2025 12:00:00 AM EST -05 |     4
 Sun Jan 12 2025 12:00:00 AM EST -05 |     4
 Mon Jan 13 2025 12:00:00 AM EST -05 |     8
 Tue Jan 14 2025 12:00:00 AM EST -05 |     6
 Wed Jan 15 2025 12:00:00 AM EST -05 |     8
(32 rows)
```

### Past Week

Number of seizures per day, during the past one (1) week.

```sql
seizures=> SELECT
   DATE_SERIES::DATE AS "Date",
   COUNT(seizures.timestamp) AS "Count"
FROM
    GENERATE_SERIES(
        CURRENT_DATE - INTERVAL '1 WEEK',
        CURRENT_DATE,
        '1 DAY'::INTERVAL
     ) AS DATE_SERIES
    LEFT JOIN seizures ON seizures.timestamp::DATE = DATE_SERIES::DATE
GROUP BY "Date" ORDER BY "Date";

    Date    | Count
------------+-------
 2025-08-25 |     6
 2025-08-26 |    14
 2025-08-27 |     6
 2025-08-28 |    10
 2025-08-29 |    14
 2025-08-30 |    12
 2025-08-31 |    23
 2025-09-01 |    11
(8 rows)
```

### Timespan

Oldest, and newest, seizure timestamps over all time.

```sql
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

                  Oldest                   |                  Latest
-------------------------------------------+-------------------------------------------
 Sunday    Dec 12 2021 10:02:31 PM EST -05 | Monday    Sep 01 2025 05:56:53 PM EDT -04
(1 row)
```

## Total

Total number of seizures, over all time.

```sql
seizures=> SELECT
    TO_CHAR(
        COUNT(timestamp),
        'FM9,999,999'
    ) AS "Total Seizures"
FROM seizures;

 Total Seizures
----------------
 11,246
(1 row)
```
