import datetime
from flask import Flask, flash, request, Response, make_response, render_template, redirect, url_for, send_from_directory
import influxdb
import os
import pytz
import settings
import urllib

# Run
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Static content
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Error handling
@app.errorhandler(400)
def bad_request(message):
    return error(message=message, category='fatal', code=400)

@app.errorhandler(404)
def page_not_found(message):
    return error(message=message, code=404)

@app.errorhandler(500)
def internal_server_error(message):
    return error(message=message, category='fatal', code=500)

@app.errorhandler(501)
def method_not_implemented(message):
    return error(message=message, category='fatal', code=501)

@app.errorhandler(503)
def service_unavailable(message):
    return error(message=message, category='fatal', code=503)

def error(message='Sorry! There was an error. Please try again or come back later.', category='warn', code=500):
    flash(message, category)
    return make_response(render_template('seizures.html.j2'), code)


# Create a function to get today's date in YYYY-MM-DD format in my time zone
def today():
    try:
        tz  = pytz.timezone(settings.timezone)
        dt  = datetime.datetime.today().astimezone(tz).strftime('%Y-%m-%d')
        return dt
    except Exception as e:
        print(f"today:\n{e}")
        return None


# Create context processor to make today's date and timespans available to Jinja
@app.context_processor
def injects():
    return dict(
                today       = today(),
                timespans   = settings.timespans
            )


# Create a template filter function for Jinja2 to convert ISO date to human-readable in my timezone
@app.template_filter()
def get_dow(date=None):

    if date and len(date) == 10:
        try:
            dt          = datetime.date.fromisoformat(date)
            date_url    = url_for('view_date', date=date)
            format      = f"<a href=\"{date_url}\">%a, %b %d, %Y</a>"
            return dt.strftime(format)

        except Exception as e:
            print(f"get_dow: {date}\n{e}")
            return time

    return False


# Create a template filter function for Jinja2 to convert InfluxDB timestamps to human-readable in my timezone
@app.template_filter()
def format_datetime(time=None):
    try:
        tz          = pytz.timezone(settings.timezone)
        stime       = str(time)
        unix_time   = stime[0:10]
        ftime       = datetime.datetime.fromtimestamp(int(unix_time)).astimezone(tz)
        date_url    = url_for('view_date', date=ftime.strftime('%Y-%m-%d'))
        event_url   = url_for('view_event', event=time)
        format      = f"<a href=\"{date_url}#{unix_time}\" title=\"%a, %b %d, %Y\">%a, %b %d, %Y</a> " \
                            f"@ <a href=\"{event_url}\" title=\"%I:%M:%S %p\">%I:%M:%S %p</a>"
        return ftime.strftime(format)

    except Exception as e:
        print(f"format_datetime: {time}\n{e}")
        return time


# Create a function to connect to InfluxDB
def dbc(username=settings.influxdb['username'], password=settings.influxdb['password']):
    try:
        return influxdb.InfluxDBClient(
                host        = '127.0.0.1',
                port        = 8086,
                username    = username,
                password    = password,
                ssl         = False,
                verify_ssl  = False
            )
    except Exception as e:
        print(f"connecting: {client}\n{e}")
        return e


# Create a function to clean up the JSON URL-encoded strings, with backslashed spaces for InfluxDB
def clean_name(name=None):
    try:
        return urllib.parse.unquote(name).replace(u'\xa0', u' ').replace(u"’", u"'").replace("\n", ', ')
    except Exception as e:
        print(f"clean_name: {name}\n{e}")
        return name


# Create a function to parse the JSON that we received from add()
def parse(data):
    try:

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

    except Exception as e:
        print(f"parse: {data}\n{e}")
        return data

# Handle requests for specific events ("permalinks")
@app.route('/event/<int:event>', methods=['GET'])
def view_event(event=None):

    try:
        if event and len(str(event)) == 19:
            return index(query_where = f"time = {event}")
        else:
            return page_not_found(message='Sorry, but that is not a valid event! Please try again later, or perform another search.')

    except Exception as e:
        print(f"view_event:\nevent: {event}\n{e}")
        return internal_server_error(message='Sorry, but there was an error processing that event! Please try again.')


# Handle time-span requests
@app.route('/span/<string:span>', methods=['GET'])
def view_span(span=None):

    try:
        if span in settings.timespans:
            return index(
                        query_where = f"time > NOW() - {span}",
                        span        = span
                    )
        else:
            return method_not_implemented(message='Sorry, but that is not a valid time-span! Please try again.')

    except Exception as e:
        print(f"view_span:\nspan: {span}\n{e}")
        return internal_server_error(message='Sorry, but there was an error processing that time-span! Please try again.')


# Handle requests for a specific date
@app.route('/date/<string:date>', methods=['GET'])
def view_date(date=None):

    try:
        # Find the start and end dates
        start   = datetime.date.fromisoformat(date)
        end     = start + datetime.timedelta(days=1)

        # Do not proceed with dates that are in the future
        if start > datetime.date.today():
            raise ValueError(f"Future date (date: '{date}') requested")

        # Find the offset of my timezone and add a colon separator for InfluxDB
        offset      = datetime.datetime.now(pytz.timezone(settings.timezone)).strftime('%z')
        offset_adj  = offset[0:3] + ':' + offset[3:6]

        # Format the start and end dates into strings for InfluxDB querying, with the appropriate offset
        format  = f"%Y-%m-%dT%H:%M:%S.%f{offset_adj}"
        qstart  = start.strftime(format)
        qend    = end.strftime(format)

        return index(
                    query_where = f"time > '{qstart}' AND time < '{qend}'",
                    date        = start.isoformat()
                )

    except Exception as e:
        print(f"view_date:\ndate: {date}\n{e}")
        return bad_request(message='Sorry, but that does not seem to be a valid date! Please try again.')


# Create a function for the main/index page
@app.route('/', methods=['GET'])
def index(query_where=None, date=None, span=None):

    # Set a default action
    if not query_where:
        return redirect(
                    url_for('view_date',
                        date = today()
                    )
                )

    # Build the query and always sort
    query = f"SELECT * FROM \"{settings.influxdb['measurement']}\" WHERE {query_where} ORDER BY time DESC"

    # Connect to InfluxDB, query, get results, and disconnect
    try:
        client  = dbc()
        results = client.query(
                        query,
                        database=settings.influxdb['database'],
                        epoch='ns'
                    )
        points  = results.get_points(measurement=settings.influxdb['measurement'])

    except Exception as e:
        print(f"querying:\n{e}")
        return internal_server_error('Sorry! Unfortunately, your query failed. Please try again later, or perform another search.')

    finally:
        client = None

    # Prepare and return the page of results
    try:

        # Convert results to a list and count them
        list_points     = list(points)
        points_count    = len(list_points)

        # Change HTTP response code and return a pretty message if there are no results
        if points_count > 0:
            code = 200
        else:
            return page_not_found('Sorry, but no seizures were found! Please try again later, or perform another search.')

        # Return Jinja2 template and HTTP header with the result count
        r = make_response(
                render_template('seizures.html.j2',
                    points              = list_points,
                    date                = date,
                    span                = span,
                    googlemaps_api_key  = settings.googlemaps_api_key
                ),
                code
            )
        r.headers.set('X-Result-Count:', str(points_count))
        return r

    except Exception as e:
        print(f"index:\n{e}")
        return internal_server_error('Sorry! Unfortunately the results could not be returned. Please try another search.')


# Create a function to insert to InfluxDB
@app.route('/add', methods=['POST'])
def add():

    # Drop non-JSON requests
    if request.is_json is False:
        return bad_request(message='Sorry! Invalid request.')

    # Receive and parse JSON HTTPS POST request
    try:
        data = dict(request.get_json())

        # Determine device name value for InfluxDB, and fail if it is missing
        if 'device' in data and isinstance(data['device'], str) and data['device'] != '' and data['device'] is not None:
            device  = clean_name(data['device']).replace(' ', '\\ ')
            del(data['device'])
        else:
            return bad_request(message='Sorry! Invalid device.')

        # Determine network value for InfluxDB: prefer Wi-Fi SSID from the JSON POST, otherwise just use the IP address
        if 'ssid' in data and isinstance(data['ssid'], str) and data['ssid'] != '' and data['ssid'] is not None:
            network = clean_name(data['ssid']).replace(' ', '\\ ')
        else:
            network = request.remote_addr
        del(data['ssid'])

        # Parse the fields in the request
        fields      = parse(data)

    except Exception as e:
        print(f"invalid request:\n{data}\n{e}")
        return bad_request(message='Sorry! Invalid request.')

    # Connect to InfluxDB, insert, and disconnect
    try:
        client      = dbc()
        write_data  = f"{settings.influxdb['measurement']},device=\"{device}\",network=\"{network}\" {fields}"
        if client.write(write_data, params={'db': settings.influxdb['database']}, protocol='line'):
            return Response(response='OK', status=201)

    except Exception as e:
        print(f"writing:\n{write_data}\n{client}\n{e}")
        return internal_server_error(message='Sorry! Unfortunately, the database insertion failed.')

    finally:
        client = None
