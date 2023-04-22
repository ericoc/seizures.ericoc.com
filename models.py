#!/usr/bin/env python3
"""Seizure SQLAlchemy object definition"""
from datetime import datetime, timezone
import ipaddress
import logging
import pytz
from zoneinfo import *
from sqlalchemy import Column, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import DECIMAL, TINYINT
from database import Base  # , db_session, metadata


logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s'
)


class Seizure(Base):
    __tablename__ = 'seizures'

    timestamp = Column(TIMESTAMP, primary_key=True, server_default=text("current_timestamp()"), comment='UTC Timestamp of the event')
    ssid = Column(String(32), comment='Optional name of the wireless network SSID')
    device = Column(String(32), comment='Optional name of the device')
    ip_address = Column(Text, nullable=True, comment='IP address of the request')
    latitude = Column(DECIMAL(20, 15), nullable=False, comment='GPS Latitude')
    longitude = Column(DECIMAL(20, 15), nullable=False, comment='GPS Longitude')
    address = Column(Text, comment='Optional address/location text')
    battery = Column(TINYINT(1), comment='Optional battery (between 1 and 100)')
    brightness = Column(DECIMAL(20, 15), comment='Optional brightness (between 0 and 1)')
    volume = Column(DECIMAL(20, 15), comment='Optional volume (between 0 and 1)')
    altitude = Column(DECIMAL(20, 15), comment='Optional altitude in feet')

    def __init__(self):

        # Empty default values
        self.time = self.battery = self.brightness = self.volume = None
        self.altitude = self.latitude = self.longitude = None
        self.address = self.device = self.ip_address = None

        if self.time is None:
            self.time = datetime.utcnow()

        self.timestamp = self.time.replace(tzinfo=timezone.utc)

    def from_influx(self, point=None):
        """Create a seizure object from an InfluxDB point"""

        if len(str(point['time'])) == 19:
            point['time'] = str(point['time'])[0:10]
        self.time = datetime.fromtimestamp(int(point['time']))
        self.timestamp = self.time.replace(tzinfo=ZoneInfo('America/New_York'))
        self.timestamp = self.timestamp.astimezone(pytz.timezone('Etc/UTC'))

        if point['device']:
            self.device = point['device'].replace('"', '').replace('"', '')

        point['network'] = point['network'].replace('"', '').replace('"', '')
        if '.' in point['network'] or ':' in point['network']:
            self.ip_address = self.parse_ip_address(ip_address=point['network'])
        else:
            self.ssid = point['network']

        self.latitude = point['latitude']
        self.longitude = point['longitude']
        self.address = point['address']
        self.battery = point['battery']
        self.brightness = point['brightness']
        self.volume = point['volume']
        self.altitude = point['altitude']

    def from_request(self, request=None):
        """Create a seizure object from a Flask (JSON POST) request"""

        self.time = datetime.utcnow()
        self.timestamp = self.time.replace(tzinfo=timezone.utc)
        self.ip_address = self.parse_ip_address(ip_address=request.remote_addr)

        data = request.get_json()
        self.device = data.get('device')
        self.ssid = data.get('network')
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')
        self.address = data.get('address')
        self.battery = data.get('battery')
        self.brightness = data.get('brightness')
        self.volume = data.get('volume')
        self.altitude = data.get('altitude')

    @staticmethod
    def parse_ip_address(ip_address=None):
        """Parse IP address value, whether v4 or v6"""
        try:
            ip_address = ipaddress.ip_address(ip_address)
            if isinstance(ip_address, ipaddress.IPv4Address):
                return f'::{ip_address}'
            return ip_address

        except ValueError as ip_exc:
            logging.exception(ip_exc)
            return None

    @property
    def ctime(self):
        """Format timestamp of the seizure object"""
        if isinstance(self.timestamp, datetime):
            if self.timestamp.tzinfo:
                return self.timestamp.strftime('%c %Z')
            return self.timestamp.strftime('%c')
        return self.timestamp

    def __repr__(self):
        return (f'<Seizure> {repr(self.device)} @ '
                f'{repr(self.ctime)} ({repr(self.address)})')
