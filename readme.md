# seizures.ericoc.com

This is the source code for `seizures.ericoc.com`.

_However, the website itself is for authorized users only_

## Background

I have been using an Apple Shortcut to interact with this custom-built web API.
This is extraordinarily helpful so that I can track when, and where, I have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook with just two clicks.

## Technical

Not only did I create this to track epileptic seizures, but it is also an ongoing
personal project to further my programming and general web development skills.

So, here are the juicy technical details of how it all works.

Changes made to the configuration of _any_ Apple Shortcut are shared via iCloud automatically.

Every time that I run the Apple shortcut, it sends an HTTPS JSON request to this application,
which writes a bunch of neat data to MySQL, including:
- Timestamp (UTC)
- Device Name
- Device Type
- IP address
- SSID (not sent by Apple Watch)
- Altitude (not sent by MacBook)
- Latitude
- Longitude
- Address (according to Apple)
- Battery
- Brightness
- Volume

Prior to mid-April 2023, data was stored in an InfluxDB measurement via line protocol.
In InfluxDB, the IP address was not always stored, but rather a `network` tag, of either:
- Wi-Fi SSID of the device
- Alternatively, the IP address of the device, if SSID was not found

The data is collected on the device and sent in a JSON payload to this application's `/add` end-point,
where it is processed and stored in PostgreSQL using SQLAlchemy.

With latitude and longitude, I use the Google Maps JavaScript API.
This allows me to precisely map where each one of my seizures took place,
and list them by time on this mobile-friendly website for later review/analysis.

### Database

I felt like InfluxDB was originally a good choice for this project to learn more about the technology and its functionality as a time-series database.

However, I am more comfortable with MySQL, and was not ready for InfluxDB 2.0, so I began using MariaDB with SQLAlchemy in mid-April 2023. As of July 2023, I am migrating to PostgreSQL, possibly eventually with PostGIS.

The current table schema can be found at [seizures.sql](seizures.sql)

### Maps & Web

Google Maps and its [JavaScript API](https://developers.google.com/maps/documentation/javascript/overview) are highly popular and simple to get started with.

The website depends upon nginx, uwsgi, Python, the Django framework, along with a PostgreSQL database.
I am always trying to improve my Python skills, and have been trying to get comfortable with Django.
This project previously existed as a single-file Flask app.
