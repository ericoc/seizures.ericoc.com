# coding: utf-8
from sqlalchemy import ARRAY, Column, DateTime, Numeric, String, text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Seizure(Base):
    __tablename__ = 'seizures'

    timestamp = Column(DateTime(True), primary_key=True, server_default=text("CURRENT_TIMESTAMP"))
    device_name = Column(ARRAY(String(length=32)), nullable=False)
    device_type = Column(ARRAY(String(length=32)), nullable=False)
    ip_address = Column(INET, nullable=False)
    ssid = Column(String(32))
    location = Column(NullType, nullable=False)
    altitude = Column(Numeric(20, 15), nullable=False)
