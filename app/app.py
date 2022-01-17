from flask import Flask, request, Response, make_response, render_template, redirect, url_for, send_from_directory
from datetime import datetime
import settings
import influxdb
import urllib
import pytz
import os

# Run
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

# Static content
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(message):
    return error(message, 404)

@app.errorhandler(500)
def internal_server_error(message):
    return error(message, 500)

@app.errorhandler(501)
def internal_server_error(message):
    return error(message, 501)

@app.errorhandler(503)
def service_unavailable(message):
    return error(message, 503)

def error(message='Sorry! There was an error. Please try again or come back later.', code=500):
    r = make_response(render_template('view.html.j2',
            points=None,
            timespans=settings.timespans,
            span=None,
            googlemaps_api_key=None,
            start=settings.start,
            error_message=message),
        code)
    return r

# Create a template filter function for Jinja2 to convert InfluxDB timestamps to human-readable in my timezone
@app.template_filter()
def format_datetime(time=None):
    if time:
        try:
            tz = pytz.timezone(settings.timezone)
            time = str(time)
            unix_time = time[0:10]
            format='%a, %b %d, %Y @ %I:%M:%S %p'
            return datetime.fromtimestamp(int(unix_time)).astimezone(tz).strftime(format)
        except Exception as e:
            print(f"format_datetime: {time}\n{e}")
            return time
    else:
        return False

# Create a function to connect to InfluxDB
def dbc(username, password):
    try:
        client = influxdb.InfluxDBClient(
            host='127.0.0.1',
            port=8086,
            username=username,
            password=password,
            ssl=False,
            verify_ssl=False
        )
        return client
    except Exception as e:
        print(f"connecting: {client}\n{e}")
        return e

# Create a function to clean up the JSON URL-encoded strings, with backslashed spaces for InfluxDB
def clean_name(name=None):
    if name:
        try:
            return urllib.parse.unquote(name).replace(u'\xa0', u' ').replace(u"’", u"'").replace("\n", ', ')
        except Exception as e:
            print(f"clean_name: {name}\n{e}")
            return name
    else:
        return False

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

# Handle requests for specific events ("permalinks")
@app.route('/event/<int:event>', methods=['GET'])
def view_event(event=None):
    try:
        int(event)
        query = f"SELECT * FROM \"{settings.influxdb['measurement']}\" WHERE time = {event}"
    except:
        query = None
    return index(query)

# Handle requests for a specific date
@app.route('/date/<string:date>', methods=['GET'])
@app.route('/date/<string:date>/<int:limit>', methods=['GET'])
def view_date(date=None):
    try:
        datetime.strptime(date,'%Y-%m-%d')
        query = f"SELECT * FROM \"{settings.influxdb['measurement']}\" WHERE time > '{date}T00:00:00Z' AND time < '{date}T23:59:59Z'"
    except:
        query = None
    return index(query, limit=limit)

# Handle time-span requests
@app.route('/span/<string:span>', methods=['GET'])
@app.route('/span/<string:span>/<int:limit>', methods=['GET'])
def view_span(span=settings.default_timespan,  limit=None):
    try:
        if span not in settings.timespans:
            return error(message='Sorry, but that is not a valid time span! Please try again.', code=501)
        query = f"SELECT * FROM \"{settings.influxdb['measurement']}\" WHERE time > NOW() - {span}"
    except:
        query = None
    return index(query, limit=limit, span=span)

@app.route('/', methods=['GET'])
def index(query=None, limit=None, span=None):

    # Set a default query if none was provided and modify any query to sort results and append any limit
    if not query:
        return view_span()
    query += ' ORDER BY time DESC'
    if limit:
        query += f" LIMIT {limit}"

    # Connect to InfluxDB
    try:
        client = dbc(settings.influxdb['username'], settings.influxdb['password'])
    except:
        return error(message='Sorry! Unfortunately, the database is offline. Please try again later.', code=503)

    # Query InfluxDB, get results, and disconnect
    try:
        results = client.query(query, database=settings.influxdb['database'], epoch='ns')
        points = results.get_points(measurement=settings.influxdb['measurement'])
        client = None
    except Exception as e:
        print(f"querying: {query}\n{e}")
        return error('Sorry! Unfortunately, your query failed. Please try again later, or perform another search.', 500)

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
        r = make_response(render_template('view.html.j2',
                points=list_points,
                timespans=settings.timespans,
                span=span,
                googlemaps_api_key=settings.googlemaps_api_key,
                start=settings.start),
            code)
        r.headers.set('X-Result-Count:', str(points_count))
        return r

    except Exception as e:
        print(f"returning: {points}\n{r}\n{e}")
        return error(message='Sorry! Unfortunately the results could not be returned. Please try another search.', code=500)

# Create a function to insert to InfluxDB
@app.route('/add', methods=['POST'])
def add():

    # Drop non-JSON requests
    if request.is_json is False:
        return error(message='Sorry! Invalid request.', code=400)

    # Receive and parse JSON HTTPS POST request
    try:
        data = dict(request.get_json())

        # Determine device name value for InfluxDB, and fail if it is missing
        if 'device' in data and isinstance(data['device'], str) and data['device'] != '' and data['device'] is not None:
            device = clean_name(data['device']).replace(' ', '\\ ')
            del(data['device'])
        else:
            return error(message='Sorry! Invalid device.', code=400)

        # Determine network value for InfluxDB: prefer Wi-Fi SSID from the JSON POST, otherwise just use the IP address
        if 'ssid' in data and isinstance(data['ssid'], str) and data['ssid'] != '' and data['ssid'] is not None:
            network = clean_name(data['ssid']).replace(' ', '\\ ')
        else:
            network = request.remote_addr
        del(data['ssid'])

    except Exception as e:
        print(f"invalid request:\n{data}\n{e}")
        return error(message='Sorry! Invalid request.', code=400)

    # Parse the rest of the fields received to build a line protocol statement for InfluxDB
    try:
        fields = parse(data)
    except:
        return error(message='Sorry! There was a failure parsing the request.', code=500)

    # Connect to InfluxDB
    try:
        client = dbc(settings.influxdb['username'], settings.influxdb['password'])
    except:
        return error(message='Sorry! Unfortunately, the database is offline. Please try again later.', code=503)

    # Insert the data to InfluxDB
    try:
        write_data = f"{settings.influxdb['measurement']},device=\"{device}\",network=\"{network}\" {fields}"
        if client.write(write_data, params={'db': settings.influxdb['database']}, protocol='line'):
            return Response(response='OK', status=201)
    except Exception as e:
        print(f"writing:\n{write_data}\n{client}\n{e}")
        return error(message='Sorry! Unfortunately, the insertion failed.', code=500)
