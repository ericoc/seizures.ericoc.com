# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

While the website itself is for authorized users only, there are a few example
screenshots below!

## Background

I use an Apple Shortcut to track when - and where - I have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook
with just two (2) taps. Less detailed events can also be added in a browser.

The Apple Watch shortcut could even _theoretically_ be used by another person,
while the watch remains on my wrist.

## Examples

Seizures are displayed three (3) different ways, demonstrated below.

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

Detailed information about each seizure is listed using
[DataTables](https://datatables.net/) which allows copying to the clipboard,
as well as exporting comma-separated values (.csv) and Microsoft Excel (.xlsx)
files.

![DataTables 2024](apps/core/static/images/datatables_2024.png)

## Technical

This is an ongoing personal project - which originally began as a small Flask
application - to further my web development skills.

The website depends upon nginx, gunicorn, Python 3.13, Django,
Django REST framework, and relies upon a local PostgreSQL database, as well as
Django QuerySets to a Snowflake database (where seizure event data is stored):

- [Django Project](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Snowflake](https://www.snowflake.com/)
- [django-snowflake](https://pypi.org/project/django-snowflake/)

### Apple Shortcut

![Apple Shortcut](apps/core/static/images/shortcut_2024.png)

When the [Apple shortcut](Add_Seizure.shortcut) is executed, the Apple device
sends an HTTPS JSON POST request to the `/api/seizures/` Django REST framework
end-point using token-based authentication in an `Authorization` header,
subsequently writing a row to the Snowflake database - a "_seizure_" -
including the following data, at the time of the event:

- Timestamp _(UTC)_
- Device Name
- Device Type
- Battery
- Brightness
- Volume
- Latitude
- Longitude


- Address
    - _According to Apple_.
- SSID
  - _Not sent by Apple Watch_.
- Altitude
  - _Not sent by MacBook_.


### Database

Seizures are stored in a Snowflake database ([schema](seizures.sql)), while
other Django data including users/permissions are stored locally in PostgreSQL.

#### History

These seizure events have been stored in numerous different databases, having
been migrated at least three (3) times - from MySQL, PostgreSQL, InfluxDB, and
now Snowflake.

In August 2023, I migrated to PostgreSQL (using Django QuerySets), but then
again migrated my Django QuerySets to query a Snowflake warehouse as of
February 2024.
