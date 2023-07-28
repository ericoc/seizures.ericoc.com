# Thoughts/Ideas

## Markers
- Should marker icons be different per device (like the emojis)
- Number markers on the map
    * `label: {{ loop.index }}` on the `marker_`
- Possibly remove labels of places on the map to reduce clutter
    * Perhaps try out [OpenStreetMap](https://www.openstreetmap.org/)

## Apple Shortcut
- Safely publish/share the Apple Shortcut (`.shortcut`) file
  - Prompt for URL, username, and password

## Voice
- Voice command from Amazon Alexa would be great
  - Probably more realistic with an Apple HomePod

- GPS on these devices
  - They do not move

### PostgreSQL JSONB
- Flask receives two JSON dictionaries from the Apple shortcut
  - Stored in PostgreSQL JSONB field(s)
    - Similarly to [https://github.com/ericoc/indego.ericoc.com/](https://github.com/ericoc/indego.ericoc.com/)


### Long-Term
- Hourly grouping
- Make more use of data, specifically:
  - `altitude`
  - `battery`
  - `brightness`
  - `network`
  - `volume`
