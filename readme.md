# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

While the website itself is for authorized users only, there are a few example
screenshots below.

---

## Background

I use an Apple Shortcut ([Add_Seizure.shortcut](Add_Seizure.shortcut)) to track
when, and where, I have epileptic seizures.

The Apple Shortcut to track a seizure can be executed from my Apple Watch,
iPad, iPhone, or Mac with just two (2) taps.
The Apple Watch shortcut could even _theoretically_ be used by another person,
while the watch remains on my wrist.

Less detailed events can also be added from a browser.

---

## Examples

Seizures are generally displayed one of three (3) different ways -
using the map, chart, or table - shown below.

### Map

The default page, after logging in, is a map of seizures displayed using
Leaflet, in combination with OpenStreetMap.

![Leaflet 2024](apps/core/static/images/leaflet_2024.png)

### Chart

Seizure frequency, per day, is charted with Highcharts.

![Highcharts 2024](apps/core/static/images/highcharts_2024.png)

### Table

Detailed information about each seizure can be listed using DataTables which
supports copying rows to the clipboard, as well as exporting
_comma-separated values_ (`.csv`) and _Microsoft Excel_ (`.xlsx`) files.

![DataTables 2024](apps/core/static/images/datatables_2024.png)

---

## Technical

### API

An HTTPS REST API is made available with Django REST framework (DRF).
Seizures are added by HTTPS POST requests to the `/api/seizures/` DRF end-point,
from the Apple Shortcut.

![Django REST framework API](apps/core/static/images/drf_example.png)

#### Apple Shortcut

When the Apple Shortcut is executed, the Apple device sends an HTTPS JSON POST
request to the `/api/seizures/` Django REST framework end-point with token-based
authentication (using an `Authorization` request header), subsequently writing
a row to the Snowflake database - a "_seizure_" - including the following data,
at the time of the event.

![Apple Shortcut](apps/core/static/images/shortcut_2024.png)

- Timestamp
  - _Coordinated Universal Time (UTC)_
- Device Name
- Device Type
  - `iPhone`
  - `Mac`
  - `Watch`
  - `iPad`

- Battery
  - `0` - `100`
- Brightness
  - `0` - `1`
- Volume
  - `0` - `1`

- Latitude
- Longitude

- Address
  - According to _Apple_.
- SSID
  - Not sent by _Apple Watch_.
- Altitude
  - Measured in **meters**.
  - Not sent by _MacBook_.

### Data

Seizure event data is stored in a _Snowflake_ database
([seizures.sql](seizures.sql)) using Django QuerySets with `django-snowflake`.

All Django data, including users/permissions, is stored locally in PostgreSQL.

### Software

This web application depends upon the following software.

- [nginx](https://nginx.org/)
- [Python](https://www.python.org/)
  - [gunicorn](https://gunicorn.org/)
  - [Django web framework](https://www.djangoproject.com/)
    - [Django REST framework](https://www.django-rest-framework.org/)


- [PostgreSQL](https://www.postgresql.org/)
- [Snowflake](https://www.snowflake.com/)
  - [django-snowflake](https://pypi.org/project/django-snowflake/)


- [Leaflet](https://leafletjs.com/)
  - [OpenStreetMap](https://www.openstreetmap.org/)
- [Highcharts](https://www.highcharts.com/)
- [DataTables](https://datatables.net/)
