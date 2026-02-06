from sqlmodel import Session, select
from typing import Dict, Any, Optional
from contextlib import contextmanager
import time
import logging
from .engine import get_engine


logger = logging.getLogger(__name__)


def execute_in_transaction(session: Session, operations_func, *args, **kwargs):
    """
    Execute a function within a database transaction.

    Args:
        session: Database session
        operations_func: Function to execute within the transaction
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result of the operations function

    Raises:
        Exception: If any operation fails, the transaction is rolled back
    """
    try:
        result = operations_func(session, *args, **kwargs)
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction failed: {str(e)}")
        raise


@contextmanager
def get_temp_session():
    """
    Context manager to get a temporary database session.

    Usage:
        with get_temp_session() as session:
            # perform database operations
            session.add(obj)
            session.commit()
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


def bulk_insert(session: Session, model_class, data_list: list):
    """
    Perform a bulk insert operation.

    Args:
        session: Database session
        model_class: SQLModel class to insert
        data_list: List of dictionaries with data to insert

    Returns:
        Number of inserted records
    """
    objects = [model_class(**data) for data in data_list]
    session.add_all(objects)
    session.commit()
    return len(objects)


def get_table_row_count(session: Session, model_class) -> int:
    """
    Get the total row count for a table.

    Args:
        session: Database session
        model_class: SQLModel class representing the table

    Returns:
        Number of rows in the table
    """
    from sqlmodel import func
    stmt = select(func.count(model_class.id))
    return session.exec(stmt).one()


def measure_query_time(query_func, *args, **kwargs) -> tuple:
    """
    Measure the execution time of a query function.

    Args:
        query_func: Function to measure
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Tuple of (result, execution_time_in_seconds)
    """
    start_time = time.time()
    result = query_func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time

    logger.info(f"Query executed in {execution_time:.4f} seconds")

    return result, execution_time


def is_database_connected():
    """
    Check if the database is connected and accessible.

    Returns:
        True if database is accessible, False otherwise
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            # Try a simple query to test connection
            session.exec(select(1))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False