"""seizures.ericoc.com"""

from datetime import date, datetime
from zoneinfo import ZoneInfo
import logging

from flask import Flask, flash, redirect, Response, request, render_template, \
    url_for
from sqlalchemy import func

from database import db_session
from models import Seizure


# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configure logging
logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s',
    handlers=[logging.StreamHandler()]
)

# Set time spans and my local time zone
TIMESPANS = app.config.get('TIMESPANS')
TZNAME = app.config.get('TZNAME')
TIMEZONE = ZoneInfo(TZNAME)


def today():
    """Get today's date in my time zone"""
    return datetime.now(tz=TIMEZONE).strftime('%Y-%m-%d')


@app.context_processor
def injects():
    """Device icons, Google Maps API key,
        timespans, and today's date available to template"""
    return {
        'device_icons': app.config.get('DEVICE_ICONS'),
        'googlemaps_api_key': app.config.get('GOOGLEMAPS_API_KEY'),
        'timespans': TIMESPANS,
        'today': today()
    }


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
    category='warn', code=500,
    message='Sorry, but please try again or come back later.'
):
    """Show error message with response code"""
    flash(message=message, category=category)
    return render_template('seizures.html.j2'), code


@app.route('/event/<int:event>', methods=['GET'])
def view_event(event=None):
    """Handle requests for specific events (UNIX time permalinks)"""
    try:
        dt = datetime.fromtimestamp(event)
    except Exception as view_event_exc:
        logging.exception(view_event_exc)
        return bad_request(
            message=(
                'Sorry, but that is an invalid event! '
                'Please try again later, or perform another search.'
            )
        )

    seizures = Seizure.query.filter_by(timestamp=dt).all()
    if seizures:
        return index(seizures=seizures)

    return page_not_found(
        message=(
            'Sorry, but that event could not be found! '
            'Please try again later, or perform another search.'
        )
    )


@app.route('/span/<string:span>', methods=['GET'])
def view_span(span=None):
    """Timespan requests"""
    if span in TIMESPANS:
        start = datetime.now(tz=TIMEZONE) - TIMESPANS[span]

    if start:
        seizures = Seizure.query.filter(
            func.convert_tz(Seizure.timestamp, 'Etc/UTC', TZNAME) >= start
        ).order_by(
            Seizure.timestamp.desc()
        ).all()

        logging.info(
            'Searching span (%s): %s [%i seizures]',
            span, start, len(seizures)
        )
        return index(seizures=seizures, span=span)

    return method_not_implemented(
        message=(
            'Sorry, but that timespan is invalid! '
            'Please try again later, or perform another search.'
        )
    )


@app.route('/date/<string:when>', methods=['GET'])
def view_date(when=None):
    """Date requests"""
    try:
        dt = date.fromisoformat(when)
        seizures = Seizure.query.filter(
            func.date(
                func.convert_tz(Seizure.timestamp, 'Etc/UTC', TZNAME)
            ) == dt
        ).order_by(
            Seizure.timestamp.desc()
        ).all()
        logging.info(
            'Searching date (%s): %i seizures',
            dt, len(seizures)
        )
        return index(seizures=seizures, date=dt.isoformat())

    except Exception as view_date_exc:
        logging.exception(view_date_exc)
        return bad_request(
            'Sorry, but that is an invalid date! '
            'Please try again later, or perform another search.'
        )


@app.route('/', methods=['GET'])
def index(seizures=None, date=None, span=None):
    """Main index page"""

    if seizures is None:
        return redirect(url_for('view_date', when=today()))

    if seizures:
        return render_template(
            'seizures.html.j2', seizures=seizures, date=date, span=span
        )

    return page_not_found(
        message=(
            'Sorry, but no seizures were found! '
            'Please try again later, or perform another search.'
        )
    )


@app.route('/add', methods=['POST'])
def add():
    """Add a seizure, by inserting to MySQL database"""
    if request.is_json is False:
        logging.warning('Non-JSON request')
        return Response(response='ERR', status=400)

    try:
        seizure = Seizure()
        seizure.from_request(request=request)
        logging.info('Adding seizure:\t%s', seizure.timestamp)
        db_session.add(seizure)
        db_session.commit()
        logging.info('Added seizure:\t%s', seizure.timestamp)
        return Response(response='OK', status=201)

    except Exception as add_exc:
        logging.fatal('Add seizure:\tFAILED!')
        logging.debug('Request:\t%s', request)
        logging.debug('Seizure:\t%s', seizure.timestamp)
        logging.exception(add_exc)
        return Response(response='EXC', status=500)


@app.teardown_appcontext
def shutdown_session(shutdown_exc=None):
    """Remove database session at request teardown, and log any exception"""
    if shutdown_exc:
        logging.exception(shutdown_exc)
    db_session.remove()
