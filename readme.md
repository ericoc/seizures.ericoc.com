# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

_However, the website itself is for authorized users only_.

## Background

I have been using an Apple Shortcut to track when, and (precisely) where, I
have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook
with just a maximum of two taps.
The Apple Watch shortcut is actually even simple for someone who is with me to
use - while the watch remains on my wrist.

## Technical

Not only did I create this to track epileptic seizures, but it is also an
ongoing personal project to further my programming and general web development
skills. This originally began as a single-file Flask application. The website
depends upon nginx, gunicorn, Python 3.11, Django, Django REST Framework, and
relies upon a local PostgreSQL database, as well as Django QuerySets to a
Snowflake warehouse using: [`django-snowflake`](https://pypi.org/project/django-snowflake/).

Every time that I run the Apple shortcut, the Apple device where sends an
HTTPS JSON POST request to this application's Django REST Framework end-point.
This application writes a row to the database - which is an "event"
or "seizure", including:

- Timestamp (UTC)
- Device Name
- Device Type
- SSID (not sent by Apple Watch)
- Altitude (not sent by MacBook)
- Latitude
- Longitude
- Address (according to Apple)
- Battery
- Brightness
- Volume

The data is collected on the Apple device and sent to the `/api/seizures`
Django REST Framework end-point.

### Database

I have stored these events in numerous different databases - migrating at least
three (3) times, from MySQL, PostgreSQL, InfluxDB, and now currently Snowflake.

In August 2023, I migrated to PostgreSQL (using Django QuerySets), but then
again migrated my Django QuerySets to query a Snowflake warehouse as of
February 2024.

The current Snowflake schema can be found at: [seizures.sql](seizures.sql)

### Map

With latitude and longitude, I use [Leaflet](https://leafletjs.com/), in
combination with [OpenStreetMap](https://www.openstreetmap.org/) to precisely
map where each one of my seizures took place.
