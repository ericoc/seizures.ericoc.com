#!/usr/bin/env python3
"""Seizure SQLAlchemy object definition"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import ipaddress
import logging
import urllib

from sqlalchemy import Column, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import DECIMAL, TINYINT

from config import TZNAME
from database import Base


# Configure logging
logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s',
    handlers=[logging.StreamHandler()]
)


class Seizure(Base):
    """Seizure in the database"""
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
        """Default current time and null values"""
        self.timestamp = datetime.now(tz=timezone.utc)
        self.ssid = self.device = self.ip_address = None
        self.latitude = self.longitude = self.address = self.altitude = None
        self.battery = self.brightness = self.volume = None

    def from_request(self, request=None):
        """Create seizure object from Flask (JSON POST) request"""

        self.timestamp = datetime.now(tz=timezone.utc)
        self.ip_address = self.parse_ip_address(request.remote_addr)
        data = request.get_json()

        device = data.get('device')
        self.ssid = self.parse_field(device.get('ssid'))
        self.device = self.parse_field(device.get('name'))
        self.battery = device.get('battery')
        self.brightness = device.get('brightness')
        self.volume = device.get('volume')

        location = data.get('location')
        self.address = self.parse_field(location.get('address'))
        self.altitude = location.get('altitude')
        self.latitude = location.get('latitude')
        self.longitude = location.get('longitude')

    @staticmethod
    def parse_field(name=None):
        """Parse JSON URL-encoded string values, for database insert"""
        try:
            return urllib.parse.unquote(
                name
            ).replace(u'\xa0', u' ').replace(u"’", u"'").replace("\n", ', ')
        except Exception as e:
            logging.exception(e)
            return name

    @staticmethod
    def parse_ip_address(ip_address=None):
        """Format IPv4 address value, for database insert"""
        try:
            ip_address = ipaddress.ip_address(ip_address)
            if isinstance(ip_address, ipaddress.IPv4Address):
                return f'::{ip_address}'
            return ip_address
        except ValueError as ip_exc:
            logging.exception(ip_exc)
            return None

    @property
    def local_time(self):
        """Timestamp of the seizure in my timezone"""
        return self.timestamp.replace(
            tzinfo=timezone.utc
        ).astimezone(
            tz=ZoneInfo(TZNAME)
        )

    @property
    def unix_time(self):
        """UNIX epoch timestamp of the seizure"""
        return int(self.timestamp.timestamp())

    def __repr__(self):
        return (f'<Seizure> {repr(self.device)} @ {self.timestamp} '
                f'({self.local_time}) [{self.unix_time}]')
