# Thoughts/Ideas

## JavaScript
- Need to remove duplicated JavaScript from chart, table, and map pages.

## Snowpark

- [snowflake-snowpark-python](https://pypi.org/project/snowflake-snowpark-python/)
  - The [:datebucket() filter](https://docs.snowflake.com/en/user-guide/ui-snowsight-filters#snowsight-system-filters)
  should include dates with zero (0) seizures in its output, which will prevent
  those dates from being left off of Highcharts entirely _(as they are now)_.
  - Additionally, graph which hours of the day seizures occur most often.

## Map Markers
- Should map marker icons be numbered, or different per device (like emojis)?
  - [https://leafletjs.com/examples/custom-icons/](https://leafletjs.com/examples/custom-icons/) 
  - Emojis per device type markers were _very_ hard to actually see on the map.
    - Device type emojis seemed to blend into the map.

## Backend/Storage
- Python receives a JSON POST request from the Apple shortcut.
  - Data could be stored in JSON(B?) field(s).
    - _Similar to
      [https://github.com/ericoc/indego.ericoc.com/](https://github.com/ericoc/indego.ericoc.com/)_

## Users

- Update details/"profile":
  - First name
  - Last name
  - E-mail address
  - Password
  - Default/"main" view:
    - Chart
    - Map _(current)_
    - Table


- _"Forgot Password?"_
- _"Remember Me?"_
