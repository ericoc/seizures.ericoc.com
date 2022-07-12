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

- Add screenshots to readme.

- Publish the Apple Shortcut (`.shortcut`) file.
    * Figure out how to not share credentials though.

- Make the map stay visible when scrolling down if there are a large number of search results.
    * This is the case on desktop, but not mobile.
        - Investigate CSS `position: sticky;`.

- Eventually, execution via voice command from Amazon Alexa would be neat.
    * Probably more realistic with an Apple HomePod
        - However,not sure if such devices provide GPS coordinates, etc.

- Fix logo to be outlined white instead of purple on hover in dark mode

- Do the whole thing JSON end-to-end.
    * The payload already comes into Flask as JSON. Why decode it? Maybe other than to parse fields...
        - InfluxDB has JSON mode magic:
            ```
                > format json
                > select * from seizures where time = 1656274461204453437;
                > "results":[{"series":[{"name":"seizures","columns":["time","address","altitude","battery","brightness","device","latitude","longitude","network","volume"],"values":[[1656274461204453437,"Visionworks, 2300 S Christopher Columbus Blvd, Philadelphia PA 19148, United States",14.7422857284546,70,0,"\"Eric's Apple Watch\"",39.91581716598921,-75.13897320817036,"\"2607:fb90:2edc:1784:28ec:62b0:8053:3633\"",1]]}]}]}
            ```
