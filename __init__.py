"""seizures.ericoc.com"""

import datetime
import logging

import pytz
from flask import Flask, flash, request, Response, make_response, \
    render_template, redirect, url_for
from influxdb import InfluxDBClient

from database import db_session
from models import Seizure
from util import clean_name


logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s'
)

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.errorhandler(400)
def bad_request(message):
    """Bad Request (400)"""
    return error(message=message, category='fatal', code=400)


@app.errorhandler(404)
def page_not_found(message):
    """Page not found (404)"""
    return error(message=message, code=404)


@app.errorhandler(500)
def internal_server_error(message):
    """Internal server error (500)"""
    return error(message=message, category='fatal', code=500)


@app.errorhandler(501)
def method_not_implemented(message):
    """Method not implemented (501)"""
    return error(message=message, category='fatal', code=501)


@app.errorhandler(503)
def service_unavailable(message):
    """Service unavailable (503)"""
    return error(message=message, category='fatal', code=503)


def error(
        message=('Sorry! There was an error.'
                 'Please try again or come back later.'),
        category='warn', code=500
):
    """Show error message with response code"""
    flash(message=message, category=category)
    return make_response(render_template('seizures.html.j2'), code)


def today(tz=pytz.timezone(app.config['TIMEZONE'])):
    """Get today's date in YYYY-MM-DD format in my time zone"""
    return datetime.datetime.today().astimezone(tz).strftime('%Y-%m-%d')


@app.context_processor
def injects():
    """Today's date and timespans available to template"""
    return {'today': today(), 'timespans': app.config['TIMESPANS']}


@app.template_filter()
def get_dow(date=None):
    """Convert ISO date to human-readable in my timezone"""
    if date and len(date) == 10:
        dt = datetime.date.fromisoformat(date)
        date_url = url_for('view_date', date=date)
        return dt.strftime(f'<a href="{date_url}">%a, %b %d, %Y</a>')
    return False


@app.template_filter()
def format_datetime(time=None, tz=pytz.timezone(app.config['TIMEZONE'])):
    """Convert InfluxDB timestamps to human-readable in my timezone"""
    try:
        stime = str(time)
        unix_time = stime[0:10]
        ftime = datetime.datetime.fromtimestamp(int(unix_time)).astimezone(tz)
        date_url = url_for('view_date', date=ftime.strftime('%Y-%m-%d'))
        event_url = url_for('view_event', event=time)
        return ftime.strftime(
            f'<a href="{date_url}#{unix_time}" '
            'title="%a, %b %d, %Y">%a, %b %d, %Y</a> '
            f'@ <a href="{event_url}" title="%I:%M:%S %p %Z">%I:%M:%S %p</a>'
        )

    except Exception as e:
        logging.exception(e)
        return time


def dbc():
    """Connect to InfluxDB"""
    return InfluxDBClient(
        host='127.0.0.1', port=8086, ssl=False, verify_ssl=False,
        username=app.config['INFLUXDB_CREDS']['username'],
        password=app.config['INFLUXDB_CREDS']['password']
    )


@app.route('/event/<int:event>', methods=['GET'])
def view_event(event=None):
    """Handle requests for specific events ("permalinks")"""

    try:
        if event and len(str(event)) == 19:
            return index(query_where=f"time = {event}")
        else:
            return page_not_found(
                message=(
                    'Sorry, but that is not a valid event! '
                    'Please try again later, or perform another search.'
                )
            )

    except Exception as e:
        logging.exception(e)
        return internal_server_error(
            message=(
                'Sorry, but there was an error processing that event! '
                'Please try again.'
            )
        )


# Handle time-span requests
@app.route('/span/<string:span>', methods=['GET'])
def view_span(span=None):
    try:
        if span in app.config['TIMESPANS']:
            return index(query_where=f"time > NOW() - {span}", span=span)
        else:
            return method_not_implemented(
                message=(
                    'Sorry, but that is not a valid time-span! '
                    'Please try again.'
                )
            )

    except Exception as e:
        logging.exception(e)
        return internal_server_error(
            message=(
                'Sorry, but there was an error processing that time-span! '
                'Please try again.'
            )
        )


# Handle requests for a specific date
@app.route('/date/<string:date>', methods=['GET'])
def view_date(date=None, tz=pytz.timezone(app.config['TIMEZONE'])):
    try:
        # Find start and end dates
        start = datetime.date.fromisoformat(date)
        end = start + datetime.timedelta(days=1)

        # Do not proceed with future dates
        if start > datetime.date.today():
            raise ValueError(f"Future date (date: '{date}') requested")

        # Find my timezone offset and add a colon separator for InfluxDB
        offset = datetime.datetime.now(tz).strftime('%z')
        offset_adj = offset[0:3] + ':' + offset[3:6]

        # Format the start and end dates into strings for InfluxDB querying,
        #   with the appropriate offset
        dt_format = f"%Y-%m-%dT%H:%M:%S.%f{offset_adj}"
        qstart = start.strftime(dt_format)
        qend = end.strftime(dt_format)

        return index(
            query_where=f"time > '{qstart}' AND time < '{qend}'",
            date=start.isoformat()
        )

    except Exception as e:
        logging.exception(e)
        return bad_request(
            message=(
                'Sorry, but that does not seem to be a valid date! '
                'Please try again.'
            )
        )


@app.route('/', methods=['GET'])
def index(query_where=None, date=None, span=None):
    """Main index page"""

    # Set a default action
    if not query_where:
        return redirect(
            url_for(
                'view_date',
                date=today()
            )
        )

    # Build the query and always sort
    query = (
        f"SELECT * FROM {app.config['INFLUXDB_CREDS']['measurement']} "
        f"WHERE {query_where} "
        "ORDER BY time DESC"
    )

    client = None
    try:

        # Connect to Influx DB
        client = dbc()

        # Query InfluxDB
        results = client.query(
            query,
            database=app.config['INFLUXDB_CREDS']['database'], epoch='ns'
        )

        # Get results of InfluxDB query
        points = results.get_points(
            measurement=app.config['INFLUXDB_CREDS']['measurement']
        )

    except Exception as exc:
        logging.exception(exc)
        return service_unavailable(
            message=(
                'Sorry! Unfortunately, the database is unavailable. '
                'Please try again later, or perform another search.'
            )
        )

    finally:

        # Disconnect from InfluxDB
        if client:
            client.close()

    # Prepare and return the page of results
    try:

        # Convert results to a list and count them
        list_points = list(points)
        points_count = len(list_points)

        # Change HTTP response code
        #   and return a message if there are no results
        if points_count > 0:
            code = 200
        else:
            return page_not_found(
                message=(
                    'Sorry, but no seizures were found! '
                    'Please try again later, or perform another search.'
                )
            )

        # Return Jinja2 template and HTTP header with the result count
        r = make_response(
            render_template(
                'seizures.html.j2',
                points=list_points, date=date, span=span,
                googlemaps_api_key=app.config['GOOGLEMAPS_API_KEY']
            ), code
        )
        r.headers.set('X-Result-Count:', str(points_count))
        return r

    except Exception as e:
        logging.exception(e)
        return internal_server_error(
            message=(
                'Sorry! Unfortunately the results could not be returned. '
                'Please try another search.'
            )
        )


@app.route('/add', methods=['POST'])
def add():
    """Insert to InfluxDB"""

    # Drop non-JSON requests
    if request.is_json is False:
        return bad_request(message='Sorry! Invalid request.')

    # Receive and parse JSON HTTPS POST request
    try:
        data = dict(request.get_json())
        seizure = Seizure()
        seizure.from_request(request=request)
        print(seizure)
        logging.info(seizure)
        db_session.add(seizure)

        # Determine device name value for InfluxDB, and fail if it is missing
        if 'device' in data and data['device']:
            device = clean_name(data['device']).replace(' ', '\\ ')
            del (data['device'])
        else:
            return bad_request(message='Sorry! Invalid device.')

        # Determine network value for InfluxDB:
        #   prefer Wi-Fi SSID from the JSON POST,
        #       otherwise just use the IP address
        if 'ssid' in data and data['ssid']:
            network = clean_name(data['ssid']).replace(' ', '\\ ')
        else:
            network = request.remote_addr
        del (data['ssid'])

        # Parse the fields in the request
        fields = parse(data)

    except Exception as e:
        logging.exception(e)
        return bad_request(message='Sorry! Invalid request.')

    client = None
    try:

        # Connect to InfluxDB
        client = dbc()

        # Write/insert to InfluxDB using line protocol
        write_data = app.config['INFLUXDB_CREDS']['measurement']
        write_data += f',device="{device}",network="{network}" {fields}'
        if client.write(
                write_data,
                params={'db': app.config['INFLUXDB_CREDS']['database']},
                protocol='line'
        ):
            db_session.commit()
            logging.info('Added')
            return Response(response='OK', status=201)

    except Exception as e:
        logging.exception(e)
        return internal_server_error(
            message='Sorry! Unfortunately, the database insertion failed.'
        )

    finally:

        # Disconnect from InfluxDB
        if client:
            client.close()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown, and log any exception"""
    if exception:
        logging.exception(exception)
    db_session.remove()
