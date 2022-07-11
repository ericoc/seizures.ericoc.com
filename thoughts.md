### Thoughts/Ideas

- The map zoom level is currently hard-coded to `12`
    * Should find a way to have it be calculated, probably in the Jinja template

- Should the marker icons be different per device?
    * For example: separate icons for computer, phone, watch, or default
        - The background of the icons might need to be opaque - or have rounded corners, like the default red ones

- Possibly number the markers on the map (`label: {{ loop.index }}` on the marker)

- Possibly remove labels of places on the map or see how we can have a cleaner map
    * Maybe try out [OpenStreetMap](https://www.openstreetmap.org/)

- Add screenshots to readme

- Publish the Apple Shortcut (`.shortcut`) file
    * Figure out how to not share credentials though

- Make the map stay visible when scrolling down if there are a large number of search results
    * This is the case on desktop, but not mobile
        - Investigate CSS `position: sticky;`
