"""
Comprehensive logging configuration for the TaskMaster API.
"""
import logging
import logging.config
import os
from pathlib import Path


def setup_comprehensive_logging():
    """
    Set up comprehensive logging for the application.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Get environment-specific settings
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    app_env = os.getenv("APP_ENV", "development")

    # Determine if we're in development or production
    is_dev = app_env.lower() in ["development", "dev"]

    # Logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "()": "logging.Formatter",
                "fmt": "[%(asctime)s] %(levelname)s [PID:%(process)d] [%(name)s:%(lineno)d] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "()": "logging.Formatter",
                "fmt": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "verbose" if is_dev else "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "verbose" if is_dev else "simple",
                "filename": str(logs_dir / "app.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "verbose",
                "filename": str(logs_dir / "errors.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file", "error_file"],
                "level": log_level,
                "propagate": False
            },
            "security": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False
            },
            "api": {
                "handlers": ["file", "console"],
                "level": log_level,
                "propagate": False
            },
            "database": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": False
            },
            "auth": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

    # Set specific log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def get_logger(name: str, user_context: dict = None):
    """
    Get a logger with optional user context.

    Args:
        name: Name of the logger
        user_context: Optional context to add to log entries

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if user_context:
        # Add user context to the logger
        class ContextFilter(logging.Filter):
            def filter(self, record):
                for key, value in user_context.items():
                    setattr(record, key, value)
                return True

        logger.addFilter(ContextFilter())

    return logger


def log_api_request(
    logger_instance,
    method: str,
    endpoint: str,
    status_code: int,
    response_time: float,
    user_id: int = None,
    ip_address: str = None
):
    """
    Log API request details.

    Args:
        logger_instance: Logger instance to use
        method: HTTP method
        endpoint: API endpoint
        status_code: HTTP status code
        response_time: Response time in milliseconds
        user_id: User ID if authenticated
        ip_address: Client IP address
    """
    extra = {}
    if user_id:
        extra['user_id'] = user_id
    if ip_address:
        extra['ip_address'] = ip_address

    logger_instance.info(
        f"API request: {method} {endpoint} - Status: {status_code} - "
        f"Response time: {response_time:.2f}ms",
        extra=extra
    )


def log_security_event(
    logger_instance,
    event_type: str,
    user_id: int = None,
    ip_address: str = None,
    details: dict = None
):
    """
    Log security-related events.

    Args:
        logger_instance: Security logger instance
        event_type: Type of security event
        user_id: User ID involved
        ip_address: IP address of the request
        details: Additional event details
    """
    extra = {'event_type': event_type}
    if user_id:
        extra['user_id'] = user_id
    if ip_address:
        extra['ip_address'] = ip_address
    if details:
        extra.update(details)

    logger_instance.info(
        f"Security event: {event_type}",
        extra=extra
    )


def log_database_operation(
    logger_instance,
    operation: str,
    table: str,
    duration: float,
    success: bool = True,
    user_id: int = None
):
    """
    Log database operation details.

    Args:
        logger_instance: Database logger instance
        operation: Type of operation (SELECT, INSERT, UPDATE, DELETE)
        table: Table name
        duration: Operation duration in milliseconds
        success: Whether operation succeeded
        user_id: User ID associated with operation
    """
    extra = {'operation': operation, 'table': table, 'duration_ms': duration}
    if user_id:
        extra['user_id'] = user_id

    status = "SUCCESS" if success else "FAILED"
    logger_instance.info(
        f"Database {operation} on {table} - {status} - Duration: {duration:.2f}ms",
        extra=extra
    )


# Initialize logging when module is imported
setup_comprehensive_logging()


# Convenience functions for different loggers
def get_api_logger(user_context: dict = None):
    """Get API-specific logger."""
    return get_logger("api", user_context)


def get_security_logger(user_context: dict = None):
    """Get security-specific logger."""
    return get_logger("security", user_context)


def get_database_logger(user_context: dict = None):
    """Get database-specific logger."""
    return get_logger("database", user_context)


def get_auth_logger(user_context: dict = None):
    """Get authentication-specific logger."""
    return get_logger("auth", user_context)