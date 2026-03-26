"""
Logging configuration module
"""

import logging
import logging.config
from pathlib import Path

from app.utils.config import LoggingConfig


def setup_logging(config: LoggingConfig) -> None:
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    log_file = Path(config.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.config.fileConfig(
        "config/logging.conf",
        disable_existing_loggers=False,
    )

    # Set log level
    logging.getLogger().setLevel(getattr(logging, config.level))
