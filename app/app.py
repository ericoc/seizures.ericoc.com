from flask import Flask, request, Response, make_response, render_template, redirect, url_for
from influxdb import InfluxDBClient
import urllib
import secrets
from datetime import datetime
import pytz

# Run
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

# Create a function to connect to InfluxDB
def dbc(username, password):
    try:
        client = InfluxDBClient(
            host='127.0.0.1',
            port=8086,
            username=username,
            password=password,
            ssl=False,
            verify_ssl=False
        )
        return client
    except Exception as e:
        print(e)
        return e

# Create a function to parse the JSON that we received from add()
def parse(data):

    if not data or data == '':
        return False

    # Loop through appending each key=value to a line protocol string
    count = 0
    fields = ''
    for k, v in data.items():
        fields += f"{k}="

        # urldecode, and quote, any strings
        if isinstance(v, str):
            v = clean_name(v)
            fields += f"\"{v}\""
        else:
            fields += f"{v}"

        # Append a comma to all but the last field
        count += 1
        if count != len(data.items()):
            fields += ','

    # Return the line protocol style string of fields
    return fields

# Create a function to show the records stored in InfluxDB
@app.route('/', methods=['GET'])
@app.route('/<when>', methods=['GET'])
@app.route('/<when>/<int:limit>', methods=['GET'])
def view(when='30d', limit=None):

    # Connect to InfluxDB
    try:
        client = dbc(secrets.influxdb['username'], secrets.influxdb['password'])
    except:
        return Response(response='Cannot connect to InfluxDB', status=503)

    # Prepare to query InfluxDB
    try:

        # Begin the query and create a list of user-selectable time-spans from which to view events
        query = f"SELECT * FROM \"{secrets.influxdb['measurement']}\" WHERE time "
        timespans = ['1m', '5m', '10m', '30m', '1h', '3h', '6h', '12h', '1d', '1w', '2w', '3w', '30d', '60d', '90d', '120d', '26w', '52w']

        # Handle numeric requests as permalinks to a single event
        try:
            if len(when) != 19:
                raise
            int(when)
            query += f'='

        # Otherwise, process as time-span
        except:

            # If invalid time-span received, revert to default
            if when not in timespans:
                when = '30d'

            # Modify query for the time-span
            query += f"> NOW() -"

        # Modify the query to sort results and append any limit
        query += f" {when}"
        query += ' ORDER BY time DESC'
        if limit is not None:
            query += f" LIMIT {limit}"

    except Exception as e:
        print(f"preparing: {e}")
        return Response(response='Cannot prepare query', status=500)

    # Query InfluxDB, get results, and disconnect
    try:
        results = client.query(query, database=secrets.influxdb['database'], epoch='ns')
        points = results.get_points(measurement=secrets.influxdb['measurement'])
        client = None
    except Exception as e:
        print(f"querying: {e}")
        return Response(response='Cannot query database', status=503)

    # Return page of any results
    try:

        # Retrieve list of results and count them
        list_points = list(points)
        points_count = len(list_points)

        # Change HTTP response code if there are no results
        if points_count > 0:
            code = 200
        else:
            code = 404

        # Return Jinja2 template and HTTP header with the result count
        r = make_response(render_template('view.html.j2', points=list_points, when=when, timespans=timespans, googlemaps_api_key=secrets.googlemaps_api_key, start=secrets.start), code)
        r.headers.set('X-Result-Count:', str(points_count))
        return r

    except Exception as e:
        print(e)
        return Response(response='Could not return results', status=500)

# Create a function to insert to InfluxDB
@app.route('/add', methods=['POST'])
def add():

    # Drop non-JSON requests
    if request.is_json is False:
        return Response(response='Invalid request', status=400)

    # Receive and parse JSON HTTPS POST request
    try:
        data = dict(request.get_json())

        # Determine device name value for InfluxDB, and fail if it is missing
        if 'device' in data and isinstance(data['device'], str) and data['device'] != '' and data['device'] is not None:
            device = clean_name(data['device']).replace(' ', '\\ ')
            del(data['device'])
        else:
            return Response(response='Invalid device', status=400)

        # Determine network value for InfluxDB: prefer Wi-Fi SSID from the JSON POST, otherwise just use the IP address
        if 'ssid' in data and isinstance(data['ssid'], str) and data['ssid'] != '' and data['ssid'] is not None:
            network = clean_name(data['ssid']).replace(' ', '\\ ')
        else:
            network = request.remote_addr
        del(data['ssid'])

    except Exception as e:
        print(e)
        return Response(response='Invalid request', status=400)

    # Parse the rest of the fields received to build a line protocol statement for InfluxDB
    try:
        fields = parse(data)
    except Exception as e:
        print(e)
        return Response(response='Parse failure', status=500)

    # Connect to InfluxDB
    try:
        client = dbc(secrets.influxdb['username'], secrets.influxdb['password'])
    except:
        return Response(response='Cannot connect to InfluxDB', status=503)

    # Insert the data to InfluxDB
    try:
        write_data = f"{secrets.influxdb['measurement']},device=\"{device}\",network=\"{network}\" {fields}"
        if client.write(write_data, params={'db': secrets.influxdb['database']}, protocol='line'):
            return Response(response='OK', status=201)
    except Exception as e:
        print(e)
        return Response(response='Cannot write to database', status=500)

# Create a function to clean up the JSON URL-encoded strings, with backslashed spaces for InfluxDB
def clean_name(name=None):
    if name:
        try:
            return urllib.parse.unquote(name).replace(u'\xa0', u' ').replace(u"’", u"'").replace("\n", ', ')
        except:
            print(e)
            return name
    else:
        return False

# Create a template filter function for Jinja2 to convert InfluxDB timestamps to human-readable in my timezone
@app.template_filter()
def format_datetime(time=None):
    if time:
        try:
            tz = pytz.timezone(secrets.timezone)
            time = str(time)
            unix_time = time[0:10]
            return datetime.fromtimestamp(int(unix_time)).astimezone(tz).strftime('%a, %b %d, %Y @ %I:%M:%S %p')
        except Exception as e:
            print(f"format_datetime: {time}\n{e}")
            return time
    else:
        return False
