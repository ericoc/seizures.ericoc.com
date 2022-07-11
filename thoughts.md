### Thoughts/Ideas

- The map zoom level is currently hard-coded to `12`.
    * Find a nice way to calculate zoom level, probably in the Jinja template.

- Should the marker icons be different per device?
    * For example: separate icons for computer, phone, watch, or default.
        - The background of the icons might need to be opaque - or have rounded corners, like the default red ones.

- Possibly number the markers on the map (`label: {{ loop.index }}` on the marker).

- Possibly remove labels of places on the map or reduce clutter.
    * Perhaps try out [OpenStreetMap](https://www.openstreetmap.org/)?

- Add screenshots to readme.

- Publish the Apple Shortcut (`.shortcut`) file.
    * Figure out how to not share credentials though.

- Make the map stay visible when scrolling down if there are a large number of search results.
    * This is the case on desktop, but not mobile.
        - Investigate CSS `position: sticky;`.

- Eventually, execution via voice command from Amazon Alexa would be neat.
    * Probably more realistic with an Apple HomePod, however not sure if such devices provide GPS coordinates, etc.
