from datetime import timedelta


DEBUG = True
DEVICE_ICONS = {
    "Eric's MacBook Pro": '💻',
    "Eric's iPhone": '📱',
    "Eric's Apple Watch": '⌚'
}
SECRET_KEY = 'SECRET'
GOOGLEMAPS_API_KEY = 'SECRET'
SQLALCHEMY_ECHO = True
SQLALCHEMY_URL = 'mysql+pymysql://username:password@localhost/seizures'
TZNAME = 'US/Eastern'
TIMESPANS = {
    '1m': timedelta(minutes=1),
    '5m': timedelta(minutes=5),
    '10m': timedelta(minutes=10),
    '30m': timedelta(minutes=30),
    '1h': timedelta(hours=1),
    '3h': timedelta(hours=3),
    '6h': timedelta(hours=6),
    '12h': timedelta(hours=12),
    '1d': timedelta(days=1),
    '2d': timedelta(days=2),
    '3d': timedelta(days=3),
    '4d': timedelta(days=4),
    '5d': timedelta(days=5),
    '1w': timedelta(weeks=1),
    '2w': timedelta(weeks=2),
    '3w': timedelta(weeks=3),
    '30d': timedelta(days=30),
    '60d': timedelta(days=60),
    '90d': timedelta(days=90),
    '120d': timedelta(days=120),
    '26w': timedelta(weeks=26),
    '1y': timedelta(weeks=52),
    '2y': timedelta(weeks=104),
    '3y': timedelta(weeks=156)
}
