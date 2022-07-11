### Thoughts/Ideas

- Zoom is currently hard-coded to 12, but I should calculate it (in Jinja probably)

- Should the marker icons be different per device?
    * For example, separate computer/phone/watch/default icons
        - The background of the icons might need to be opaque - or have rounded corners, like the default red ones

- Possibly number the markers on the map (`label: {{ loop.index }}` on the marker)

- Possibly remove labels of places on the map or see how we can have a cleaner map
    * Maybe even switch try out [OpenStreetMap](https://www.openstreetmap.org/)?
