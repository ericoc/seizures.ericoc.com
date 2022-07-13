# seizures.ericoc.com

## Background

I have been using an Apple Shortcut to interact with this custom-built web API.
This is extraordinarily helpful so that I can track when, and where, I have epileptic seizures!

The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook with just two clicks.

## Technical

Not only did I create this to track epileptic seizures, but it is also a on-going
personal project to further my Python, Flask, InfluxDB, and general web development skills.

So, here are the juicy technical details of how it all works.

Changes made to the configuration of any Apple Shortcut are shared via iCloud automatically.

Every time that I run the Apple shortcut, it writes a bunch of neat data to an InfluxDB measurement, including:
- Device name
- Latitude
- Longitude
- Altitude
- Battery
- Volume
- Brightness
- Network identifier, either:
    * The current Wi-Fi SSID that the device is connected to and using
    * Alternatively, the IP address of the device, if Wi-Fi is not connected

The data is collected on the device and sent in a JSON payload to this Flask application's `/add` end-point,
where it is processed and stored in InfluxDB via line protocol.

Fun fact: changes made to the configuration of any Apple Shortcut are shared via iCloud automatically.

With latitude and longitude in InfluxDB, I use the Google Maps JavaScript API
This allows me to precisely map where each and every one of my seizures took place,
and list them by time (to the nano-second!) on this mobile-friendly website for later review/analysis.

### Database

I felt like InfluxDB was a good choice for this project to learn more about the technology
and its functionality as a time-series database.

InfluxDB also works very well with Grafana and is highly accessible via the command-line interface using the `influxdb` client.

#### Alternatives?

TimescaleDB, Prometheus, or maybe Graphite could be neat to try, but I am really not interested in migrating the data at this point.
However, an interesting experiment could be to store the incoming JSON payload into a PostgreSQL JSON field as-is.

### Maps

Google Maps and its [JavaScript API](https://developers.google.com/maps/documentation/javascript/overview) are highly popular
    and simple to get started with, but I would like to try out [OpenStreetMap](https://www.openstreetmap.org/) at some point.

### Web

The website depends upon uwsgi, Python, and the Flask framework using Jinja2 templating.
Lately, I have been trying to constantly improve my Python skills, and I adore the simplicity of the Flask framework.
