"""seizures.ericoc.com"""

from datetime import date, datetime
import logging

from flask import Flask, flash, redirect, Response, request, render_template, \
    url_for
from sqlalchemy import func

from database import db_session
from models import Seizure


logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s'
)

app = Flask(__name__)
app.config.from_pyfile('config.py')

TIMESPANS = app.config['TIMESPANS']
TIMEZONE = app.config['TIMEZONE']


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


def today():
    """Get today's date in YYYY-MM-DD format, in my time zone"""
    return datetime.today().astimezone(tz=TIMEZONE).strftime('%Y-%m-%d')


@app.context_processor
def injects():
    """Google Maps API key and timespans available to template"""
    return {
        'googlemaps_api_key': app.config['GOOGLEMAPS_API_KEY'],
        'timespans': app.config['TIMESPANS']
    }


@app.route('/event/<int:event>', methods=['GET'])
def view_event(event=None):
    """Handle requests for specific events ("permalinks")"""
    seizures = Seizure.query.filter_by(
        timestamp=datetime.fromtimestamp(event)
    ).order_by(
        Seizure.timestamp.desc()
    ).all()

    if seizures:
        return index(seizures=seizures)

    return page_not_found(
        message=(
            'Sorry, but that is not a valid event! '
            'Please try again later, or perform another search.'
        )
    )


@app.route('/span/<string:span>', methods=['GET'])
def view_span(span=None):
    """Timespan requests"""
    if span in TIMESPANS:
        ago = datetime.now() - TIMESPANS[span]
        seizures = Seizure.query.filter(
            Seizure.timestamp >= ago
        ).order_by(
            Seizure.timestamp.desc()
        ).all()
        return index(seizures=seizures, span=span)

    return method_not_implemented(
        message='Sorry, but that timespan is invalid! Please try again.'
    )


@app.route('/date/<string:when>', methods=['GET'])
def view_date(when=None):
    """Date requests"""
    try:
        dt = date.fromisoformat(when)
        seizures = Seizure.query.filter(
            func.date(Seizure.timestamp) == dt
        ).order_by(
            Seizure.timestamp.desc()
        ).all()
        return index(seizures=seizures, date=dt.isoformat())

    except Exception as e:
        logging.exception(e)
        return bad_request('Sorry, that date is invalid! Please try again.')


@app.route('/', methods=['GET'])
def index(seizures=None, date=None, span=None):
    """Main index page"""
    if seizures is None:
        return redirect(url_for('view_date', when=today()))

    # Return Jinja2 template if there are results
    if seizures and len(seizures) > 0:
        return render_template(
            'seizures.html.j2',
            seizures=seizures, date=date, span=span, today=today()
        )

    # Otherwise, return 404 if no results
    return page_not_found(
        message=(
            'Sorry, but no seizures were found! '
            'Please try again later, or perform another search.'
        )
    )


@app.route('/add', methods=['POST'])
def add():
    """Insert to database"""

    # Drop non-JSON requests
    if request.is_json is False:
        return bad_request(message='Sorry! Invalid request.')

    # Receive JSON HTTPS POST request and insert to the database
    try:
        seizure = Seizure()
        print(request)
        print(request.get_json())
        seizure.from_request(request=request)
        logging.info('Adding: %s', seizure)
        db_session.add(seizure)
        db_session.commit()
        logging.info('Added.')
        return Response(response='OK', status=201)

    except Exception as e:
        logging.exception(e)
        return internal_server_error('Sorry! The database insertion failed.')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown, and log any exception"""
    if exception:
        logging.exception(exception)
    db_session.remove()
