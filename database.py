"""Database connection"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from config import SQLALCHEMY_URL, SQLALCHEMY_ECHO


class Base(DeclarativeBase):
    pass


engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
    pool_pre_ping=True
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base.query = db_session.query_property()
metadata = Base.metadata
