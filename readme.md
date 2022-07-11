# seizures.ericoc.com

## Background

- I have been using Apple Shortcuts to interact with this custom-built Flask HTTPS API, which I wrote.
    * This is extraordinarily helpful so that I can track when, and where, I have epileptic seizures!

### How it works

- Every time that I run the shortcut, it writes a bunch of neat data to an InfluxDB measurement, including:
    * Device name
    * Latitude
    * Longitude
    * Altitude
    * Battery
    * Volume
    * Brightness
    * Network identifier, either:
        - The current Wi-Fi SSID that the device is connected to and using
        - Alternatively, the IP address of the device, if Wi-Fi is not connected

- The Apple Shortcut can be executed from my iPhone, Apple Watch, or MacBook with only a single click.
    * I just tap one button and the data is collected and sent as a JSON payload to this Flask application's `/add` end-point.
    * The data is then processed and stored in InfluxDB via line protocol.

- With latitude and longitude in InfluxDB, I use the [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/overview)
    * This allows me to precisely map where each and every one of my seizures took place, and list them by time, to the nano-second.
