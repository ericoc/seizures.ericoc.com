from flask import Flask, request, Response, make_response, render_template, redirect, url_for, send_from_directory
import datetime
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

# Error handling
@app.errorhandler(404)
def page_not_found(message):
    return error(message, 404)

@app.errorhandler(500)
def internal_server_error(message):
    return error(message, 500)

@app.errorhandler(501)
def method_not_implemented(message):
    return error(message, 501)

@app.errorhandler(503)
def service_unavailable(message):
    return error(message, 503)

def error(message='Sorry! There was an error. Please try again or come back later.', code=500):
    r = make_response(render_template('seizures.html.j2',
            timespans=settings.timespans,
            error_message=message,
            today=today()),
        code)
    return r

# Create a function to get today's date in YYYY-MM-DD format in my time zone
def today():
    try:
        tz = pytz.timezone(settings.timezone)
        dt = datetime.datetime.today().astimezone(tz).strftime('%Y-%m-%d')
        return dt
    except Exception as e:
        print(f"today:\n{e}")
        return None

# Create a template filter function for Jinja2 to convert ISO date to human-readable in my timezone
@app.template_filter()
def get_dow(date=None):
    if date and len(date) == 10:
        try:
            dt = datetime.date.fromisoformat(date)
            date_url = url_for('view_date', date=date)
            format = f"<a href=\"{date_url}\">%a, %b %d, %Y</a>"
            return dt.strftime(format)
        except Exception as e:
            print(f"get_dow: {date}\n{e}")
            return time
    else:
        return False

# Create a template filter function for Jinja2 to convert InfluxDB timestamps to human-readable in my timezone
@app.template_filter()
def format_datetime(time=None):
    if time:
        try:
            tz = pytz.timezone(settings.timezone)
            stime = str(time)
            unix_time = stime[0:10]
            ftime = datetime.datetime.fromtimestamp(int(unix_time)).astimezone(tz)
            date_url = url_for('view_date', date=ftime.strftime('%Y-%m-%d'))
            event_url = url_for('view_event', event=time)
            format = f"<a href=\"{date_url}\">%a, %b %d, %Y</a> @ <a href=\"{event_url}\">%I:%M:%S %p</a>"
            return ftime.strftime(format)
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
        if event and len(str(event)) == 19:
            query_where = f"time = {event}"
            return index(query_where=query_where)
        else:
            return error(message='Sorry, but that is not a valid event! Please try again later, or perform another search.', code=404)
    except Exception as e:
        print(f"view_event:\nevent: {event}\n{e}")
        return error(message='Sorry, but there was an error processing that event! Please try again.', code=500)

# Handle time-span requests
@app.route('/span/<string:span>', methods=['GET'])
def view_span(span=None):
    try:
        if span in settings.timespans:
            query_where = f"time > NOW() - {span}"
            return index(query_where, span=span)
        else:
            return error(message='Sorry, but that is not a valid time-span! Please try again.', code=501)
    except Exception as e:
        print(f"view_span:\nspan: {span}\n{e}")
        return error(message='Sorry, but there was an error processing that time-span! Please try again.', code=500)

# Handle requests for a specific date
@app.route('/date/<string:date>', methods=['GET'])
def view_date(date=None):
    try:
        # Find the start and end dates
        start = datetime.date.fromisoformat(date)
        end = start + datetime.timedelta(days=1)

        # Find the offset of my timezone and add a colon separator for InfluxDB
        offset = datetime.datetime.now(pytz.timezone(settings.timezone)).strftime('%z')
        offset_adj = offset[0:3] + ':' + offset[3:6]

        # Format the start and end dates into strings for InfluxDB querying, with the appropriate offset
        format = f"%Y-%m-%dT%H:%M:%S.%f{offset_adj}"
        qstart = start.strftime(format)
        qend = end.strftime(format)
        query_where = f"time > '{qstart}' AND time < '{qend}'"

        return index(query_where, date=start.isoformat())

    except Exception as e:
        print(f"view_date:\ndate: {date}\n{e}")
        return error(message='Sorry, but that does not seem to be a valid date! Please try again.', code=400)

# Create a function for the main/index page
@app.route('/', methods=['GET'])
def index(query_where=None, date=None, span=None):

    # Set a default action, and always sort
    if not query_where:
        return redirect(url_for('view_span', span=settings.default_timespan))

    # Build the query and always sort
    query = f"SELECT * FROM \"{settings.influxdb['measurement']}\" WHERE {query_where} ORDER BY time DESC"

    # Connect to InfluxDB
    try:
        client = dbc(settings.influxdb['username'], settings.influxdb['password'])
    except:
        return error(message='Sorry! Unfortunately, the database is offline. Please try again later.', code=503)

    # Query InfluxDB, get results, and disconnect
    try:
        results = client.query(query, database=settings.influxdb['database'], epoch='ns')
        points = results.get_points(measurement=settings.influxdb['measurement'])

        group_query = f"SELECT COUNT(latitude) FROM \"{settings.influxdb['measurement']}\" WHERE {query_where} GROUP BY time(1d) ORDER BY time DESC TZ('{settings.timezone}')"
        group_results = client.query(group_query, database=settings.influxdb['database'])
        group_points = group_results.get_points(measurement=settings.influxdb['measurement'])
        group_list = list(group_points)
        del(group_list[-1])

    except Exception as e:
        print(f"querying:\n{e}")
        return error('Sorry! Unfortunately, your query failed. Please try again later, or perform another search.', 500)
    finally:
        client = None

    # Prepare and return the page of results
    try:

        # Convert results to a list and count them
        list_points = list(points)
        points_count = len(list_points)

        # Change HTTP response code if there are no results
        if points_count > 0:
            code = 200
        else:
            code = 404

        # Return Jinja2 template and HTTP header with the result count
        r = make_response(render_template('seizures.html.j2',
                points=list_points,
                grouped_counts=group_list,
                timespans=settings.timespans,
                date=date,
                today=today(),
                span=span,
                googlemaps_api_key=settings.googlemaps_api_key,
                start=settings.start),
            code)
        r.headers.set('X-Result-Count:', str(points_count))
        return r

    except Exception as e:
        print(f"index:\n{e}")
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

    # Connect to InfluxDB, insert, and disconnect
    try:
        client = dbc(settings.influxdb['username'], settings.influxdb['password'])
        write_data = f"{settings.influxdb['measurement']},device=\"{device}\",network=\"{network}\" {fields}"
        if client.write(write_data, params={'db': settings.influxdb['database']}, protocol='line'):
            return Response(response='OK', status=201)
    except Exception as e:
        print(f"writing:\n{write_data}\n{client}\n{e}")
        return error(message='Sorry! Unfortunately, the database insertion failed.', code=500)
    finally:
        client = None
