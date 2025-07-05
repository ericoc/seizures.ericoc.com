# Thoughts/Ideas

## JavaScript
- Need to remove duplicated JavaScript from chart, table, and map pages.

## Visualization
- Graph which hours of the day seizures occur most often.

## Map Markers
- Should map marker icons be numbered, or different per device (like emojis)?
  - [https://leafletjs.com/examples/custom-icons/](https://leafletjs.com/examples/custom-icons/) 
  - Emojis per device type markers were _very_ hard to actually see on the map.
    - Device type emojis seemed to blend into the map.

## Backend/Storage
- Python receives a JSON POST request from the Apple shortcut.
  - Data could be stored in JSON(B?) field(s).
    - _Similar to
      [https://github.com/ericoc/indego.ericoc.com/](https://github.com/ericoc/indego.ericoc.com/)_

## Queries

- Example useful queries to run.

### Device Type

```
seizures=> SELECT device_type, COUNT(device_type) AS num_seizures
seizures-> FROM seizures GROUP BY(device_type) ORDER BY num_seizures;
 device_type | num_seizures
-------------+--------------
 iPad        |            1
 Browser     |           22
 Mac         |           33
 iPhone      |           44
 Watch       |           55
(5 rows)
```

### Total

```
seizures=> SELECT COUNT(timestamp) AS total FROM seizures;
 total
-------
 155
(1 row)
```

## Users
- Update details/"profile":
  - First name
  - Last name
  - E-mail address
  - Password
  - Default/"main" view:
    - Chart
    - Map _(current)_
    - Table


- _"Forgot Password?"_
- _"Remember Me?"_
