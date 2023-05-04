#!/usr/bin/env python3
"""Seizure SQLAlchemy object definition"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import ipaddress
import logging
import urllib

from sqlalchemy import func
from sqlalchemy.dialects.mysql import DECIMAL, TINYINT, TEXT, VARCHAR
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
        default=func.now(),
        primary_key=True,
        comment='UTC Timestamp of the event'
    )
    ssid: Mapped[str] = mapped_column(
        VARCHAR(length=30),
        comment='Optional name of the wireless network SSID',
        default=None
    )
    device: Mapped[str] = mapped_column(
        VARCHAR(length=32),
        comment='Optional name of the device',
        default=None
    )
    ip_address: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        comment='IP address of the request',
        default=None
    )
    latitude: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=20, scale=15),
        nullable=False,
        comment='GPS Latitude'
    )
    longitude: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=20, scale=15),
        nullable=False,
        comment='GPS Longitude',
    )
    address: Mapped[str] = mapped_column(
        TEXT,
        comment='Optional address/location text',
        default=None
    )
    battery: Mapped[int] = mapped_column(
        TINYINT(display_width=1),
        comment='Optional battery (between 1 and 100)'
    )
    brightness: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=20, scale=15, unsigned=True),
        comment='Optional brightness (between 0 and 1)',
        default=None
    )
    volume: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=20, scale=15, unsigned=True),
        comment='Optional volume (between 0 and 1)',
        default=None
    )
    altitude: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=20, scale=15),
        comment='Optional altitude in feet',
        default=None
    )

    def from_request(self, request=None):
        """Create seizure object from Flask (JSON POST) request"""

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
                str(name)
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
