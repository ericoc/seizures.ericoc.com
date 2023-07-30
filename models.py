#!/usr/bin/env python3
"""Seizure SQLAlchemy object definition"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import ipaddress
import logging
import urllib

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Numeric, String, text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

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

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(True), primary_key=True,
        server_default=text('CURRENT_TIMESTAMP')
    )
    device_name: Mapped[str] = mapped_column(String(length=32), nullable=False)
    device_type: Mapped[str] = mapped_column(String(length=32), nullable=False)
    ip_address: Mapped[str] = mapped_column(INET, nullable=False)
    ssid: Mapped[str] = mapped_column(String(32))
    location: Mapped[tuple] = mapped_column(Geometry('POINT'))
    altitude: Mapped[int] = mapped_column(Numeric(20, 15))

    def from_request(self, request=None):
        """Create seizure object from Flask (JSON POST) request"""

        self.ip_address = self.parse_ip_address(request.remote_addr)
        data = request.get_json()

        device = data.get('device')
        self.ssid = self.parse_field(device.get('ssid'))
        self.device_name = self.parse_field(device.get('name'))
        self.device_type = device.get('type')

        location = data.get('location')
        self.location = (location.get('latitude'), location.get('longitude'))
        self.altitude = location.get('altitude')

    def from_row(self, row=None):
        """Create seizure object from CSV DictReader row"""

        self.timestamp = datetime.fromisoformat(row['timestamp']).replace(
            tzinfo=timezone.utc
        )
        self.device_name = row['device_name']
        self.device_type = row['device_type']

        self.ip_address = row['ip_address']
        if self.ip_address == 'NULL':
            self.ip_address = None

        self.ssid = row['ssid']
        if self.ssid == 'NULL':
            self.ssid = None

        self.location = (row['latitude'], row['longitude'])
        self.altitude = row['altitude']

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
        return self.timestamp.replace(tzinfo=timezone.utc).astimezone(
            tz=ZoneInfo(TZNAME)
        )

    @property
    def unix_time(self):
        """UNIX epoch timestamp of the seizure"""
        return int(self.timestamp.timestamp())

    def __repr__(self):
        return (f'<Seizure> {self.device_type} @ {self.timestamp} '
                f'({self.local_time}) [{self.unix_time}]')
