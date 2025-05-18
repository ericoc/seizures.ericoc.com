# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

While the website itself is for authorized users only, there are a few example
screenshots below!

---

## Background

This is also an ongoing personal project - which originally began as a small
Python Flask application - to further my web development skills, while also
trying my best to track my epileptic seizures accurately!

I use an Apple Shortcut to track
when, and where, I have epileptic seizures! The Apple Shortcut can be executed
from my Apple Watch, iPad, iPhone, or Mac with just two (2) taps. Less detailed
events can also be added from a browser. The Apple Watch shortcut could even
_theoretically_ be used by another person, while the watch remains on my wrist.

---

## Examples

Seizures are generally displayed three (3) different ways - map, chart,
or table - shown below.

### Map

The default page, after logging in, is a map of seizures displayed using
[Leaflet](https://leafletjs.com/), in combination with
[OpenStreetMap](https://www.openstreetmap.org/).

![Leaflet 2024](apps/core/static/images/leaflet_2024.png)

### Chart

Seizure frequency, per day, is charted with
[Highcharts](https://www.highcharts.com/).

![Highcharts 2024](apps/core/static/images/highcharts_2024.png)

### Table

Detailed information about each seizure can be listed using
[DataTables](https://datatables.net/) which supports copying rows to the
clipboard, as well as exporting _comma-separated values_ (`.csv`) and
_Microsoft Excel_ (`.xlsx`) files.

![DataTables 2024](apps/core/static/images/datatables_2024.png)

---

## Technical

The website depends upon [nginx](https://nginx.org/),
[gunicorn](https://gunicorn.org/), [Python 3.13](https://www.python.org/),
[Django](https://www.djangoproject.com/),
[Django REST framework](https://www.django-rest-framework.org/), and relies
upon a local [PostgreSQL](https://www.postgresql.org/) database, as well as
Django QuerySets to a [Snowflake](https://www.snowflake.com/) database - where
seizure event data is stored - using
[django-snowflake](https://pypi.org/project/django-snowflake/). Seizures are
stored in a Snowflake database ([schema](seizures.sql)), while all other Django
data including users/permissions are stored locally in PostgreSQL.

### API

An HTTPS REST API is available with Django REST framework (DRF). Seizures are
added by HTTPS POST requests to the `/api/seizures/` DRF end-point, from the
Apple Shortcut.

![Django REST framework API](apps/core/static/images/drf_example.png)

### Apple Shortcut

When the Apple Shortcut ([Add_Seizure.shortcut](Add_Seizure.shortcut)) is
executed, the Apple device sends an HTTPS JSON POST request to the
`/api/seizures/` Django REST framework end-point using token-based
authentication in an `Authorization` header, subsequently writing a row to the
Snowflake database - a "_seizure_" - including the following data, at the time
of the event:

![Apple Shortcut](apps/core/static/images/shortcut_2024.png)

- Timestamp _(UTC)_
- Device Name
- Device Type
  - iPhone
  - Mac
  - Watch
  - iPad
- Battery
  - 0 - 100
- Brightness
  - 0 - 1
- Volume
  - 0 - 1
- Latitude
- Longitude


- Address
    - _According to Apple_.
- SSID
  - _Not sent by Apple Watch_.
- Altitude (meters)
  - _Not sent by MacBook_.
