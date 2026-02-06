import logging
import sys
from .config import settings


def setup_logging():
    """Configure logging for the application."""
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(settings.log_level.upper()))

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Prevent duplicate logs if logging is configured elsewhere
    root_logger.propagate = False

    # Set specific loggers to WARNING level to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


# Initialize logging when module is imported
setup_logging()