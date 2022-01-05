# seizures.ericoc.com

- I have been using Apple Shortcuts to hit this sort of little custom-built Flask HTTPS API.
- Every time that I run the shortcut, it writes a bunch of neat data (including device name, latitude, longitude, altitude, battery, volume, brightness, and network SSID or IP address of the device!) to an InfluxDB measurement.
- This is extraordinarily helpful so that I can track when and where I have seizures!
- With latitude and longitude in InfluxDB, I have been using the [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/overview) and am able to create heat-maps in Grafana
