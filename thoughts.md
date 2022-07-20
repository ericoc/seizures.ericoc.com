### Thoughts/Ideas

- The map zoom level is currently hard-coded to `12`.
    * Find a nice way to calculate zoom level, probably in the Jinja template.

- Should the marker icons be different per device?
    * For example: separate icons for computer, phone, watch, or default.
        - The background of the icons might need to be opaque - or have rounded corners, like the default red ones.

- Possibly number the markers on the map, again?
    * `label: {{ loop.index }}` on the marker.

- Possibly remove labels of places on the map or reduce clutter.
    * Perhaps try out [OpenStreetMap](https://www.openstreetmap.org/)?

- Publish the Apple Shortcut (`.shortcut`) file.
    * Figure out how to not share credentials though.

- Eventually, execution via voice command from Amazon Alexa would be neat.
    * Probably more realistic with an Apple HomePod
        - However,not sure if such devices provide GPS coordinates, etc.

- Do the whole thing JSON end-to-end.
    * The payload already comes into Flask as JSON. Why decode it? Maybe other than to parse fields...
        - InfluxDB has JSON mode magic:
            ```
                > format json
                > select * from seizures where time = 1656274461204453437;
                > "results":[{"series":[{"name":"seizures","columns":["time","address","altitude","battery","brightness","device","latitude","longitude","network","volume"],"values":[[1656274461204453437,"Visionworks, 2300 S Christopher Columbus Blvd, Philadelphia PA 19148, United States",14.7422857284546,70,0,"\"Eric's Apple Watch\"",39.91581716598921,-75.13897320817036,"\"2607:fb90:2edc:1784:28ec:62b0:8053:3633\"",1]]}]}]}
            ```
        - Alternatively, PostgreSQL has JSON fields.

- Since this is a personal project and it's behind authentication live, there is not much input validation
    * `/add` only requires that the request be JSON, as well as contain `device` and `network`.
        - Otherwise, any keys/values in the JSON payload are stored in InfluxDB as-is.

Time:	1657412309163504690
Address:	Market St, Philadelphia PA 19106, United States
Altitude:	15.2203941643238
Battery:	62.0
Brightness:	0.15150760114193
Device:	"Eric's Apple Watch"
Latitude:	39.9507639930026
Longitude:	-75.15045136220301
Network:	"2607:fb90:373:ae38:4520:d19b:906c:6078"
Volume:	1.0

- I am really not doing anything with the altitude, battery, brightness, device, network, or volume.
    * I should.
    * The fields used by the website for review are just time and latitude/longitude.
        - Sorting/grouping by hour... one day
