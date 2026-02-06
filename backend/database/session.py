from sqlmodel import Session
from contextlib import contextmanager
from typing import Generator
from .engine import get_engine


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session dependency for FastAPI.

    Yields:
        Session: A SQLModel database session
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """
    Context manager for database sessions.

    Usage:
        with get_session_context() as session:
            # perform database operations
            session.add(obj)
            session.commit()
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()