# Thoughts/Ideas

## JavaScript
- Need to remove duplicated JavaScript from chart, table, and map pages.

## Visualization
- Graph which hours of the day seizures occur most often.
- Highlight, colorize, or otherwise emphasize clusters of seizures.

## Map Markers
- Should map marker icons be numbered, or different per device (emojis)?
  - [https://leafletjs.com/examples/custom-icons/](https://leafletjs.com/examples/custom-icons/) 
  - Emojis per device type markers were _very_ hard to actually see on the map.
    - Device type emojis seemed to blend into the map.

## Backend/Storage
- Python receives a JSON POST request from the Apple shortcut.
  - Data could be stored in JSON(B?) field(s).
    - _Similar to
      [https://github.com/ericoc/indego.ericoc.com/](https://github.com/ericoc/indego.ericoc.com/)_

## Queries

Some example useful database queries to run.

### Average per Day

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

### Timespan

Oldest and latest seizure dates, all time.

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

### Total

Total number of seizures, all time.

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

## Users

More (self-)user management would probably be cool
_(if this had more than one user)_.

#### Details _("Profile")_:
  - First name
  - Last name
  - E-mail address
  - Password
  - Preferences
    - Default/"main" view
      - Chart
      - Map _(current)_
      - Table

#### _"Forgot Password?"_
#### _"Remember Me?"_
