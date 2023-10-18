# seizures.ericoc.com

This is the source code for the Python Django application `seizures.ericoc.com`.

_However, the website itself is for authorized users only_.

## Background

I have been using an Apple Shortcut to track when, and where, I have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook with just two clicks.

## Technical

Not only did I create this to track epileptic seizures, but it is also an ongoing
personal project to further my programming and general web development skills.

So, here are the juicy technical details of how it all works.

Changes made to the configuration of _any_ Apple Shortcut are shared via iCloud automatically.

Every time that I run the Apple shortcut, it sends an HTTPS JSON POST request to this application,
which writes a bunch of neat data to the database, including:

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

The data is collected on the Apple device and sent to the `/api/seizures` Django REST Framework end-point.

### Database

As of August 2023, I have migrated to PostgreSQL (using Django QuerySets).

I hope to possibly use PostGIS, one day.

The current PostgreSQL schema can be found at [seizures.sql](seizures.sql)

### Maps & Web

With latitude and longitude, I use [Leaflet](https://leafletjs.com/), in combination with
[OpenStreetMap](https://www.openstreetmap.org/) to precisely map where each one of my
seizures took place.

#### Final Notes

- The website depends upon nginx, gunicorn, Python, Django with REST Framework, along with a PostgreSQL database.
- I am always trying to improve my Python skills, and have been trying to get comfortable with Django.
- This project previously existed as a single-file Flask app.
