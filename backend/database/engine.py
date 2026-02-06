from sqlmodel import create_engine
from .config import db_settings
import os


# Create the database engine with connection pooling
engine = create_engine(
    db_settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_size=20,  # Number of connection objects to maintain
    max_overflow=30,  # Additional connections beyond pool_size
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 3,
    } if "postgresql" in db_settings.DATABASE_URL else {}
)


def get_engine():
    """Return the database engine instance."""
    return engine