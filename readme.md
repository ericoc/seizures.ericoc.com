# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

_However, the website itself is for authorized users only_.


## Background

I use an Apple Shortcut to track when - and where - I have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook
with just two (2) taps. Less detailed events can also be added in a browser.

The Apple Watch shortcut could even _theoretically_ be used by another person,
while the watch remains on my wrist.


## Technical

This is an ongoing personal project - which originally began as a small Flask
application - to further my web development skills.

The website depends upon nginx, gunicorn, Python 3.13, Django,
Django REST framework, and relies upon a local PostgreSQL database, as well as
Django QuerySets to a Snowflake database (where seizures are stored):

- [Django Project](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Snowflake](https://www.snowflake.com/)
- [django-snowflake](https://pypi.org/project/django-snowflake/)


### Apple Shortcut

When the [Apple shortcut](Add_Seizure.shortcut) is executed, the Apple device
sends an HTTPS JSON POST request to the `/api/seizures/` Django REST framework
end-point, writing a row to Snowflake database - a _"seizure"_ - including:

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

These events have been stored in numerous different databases - migrating at
least three (3) times - from MySQL, PostgreSQL, InfluxDB, and now Snowflake.

In August 2023, I migrated to PostgreSQL (using Django QuerySets), but then
again migrated my Django QuerySets to query a Snowflake warehouse as of
February 2024.

The current Snowflake schema can be found at: [seizures.sql](seizures.sql)


### Chart

Seizure frequency (per day) is charted with
[Highcharts](https://www.highcharts.com/).


### Map

Seizure locations are mapped, by latitude and longitude, using
[Leaflet](https://leafletjs.com/), in combination with
[OpenStreetMap](https://www.openstreetmap.org/).
