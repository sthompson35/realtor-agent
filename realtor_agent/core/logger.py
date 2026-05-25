import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from .config import config


class LoggerSetup:
    """Centralized logging configuration"""

    _initialized = False

    @classmethod
    def setup(cls, name: Optional[str] = None) -> logging.Logger:
        """Setup and return a logger instance"""
        if not cls._initialized:
            cls._initialize_logging()
            cls._initialized = True

        return logging.getLogger(name or "realtor_agent")

    @classmethod
    def _initialize_logging(cls):
        """Initialize logging configuration"""
        log_level = getattr(logging, config.get("logging.level", "INFO"))
        log_format = config.get("logging.format")
        log_file = config.get("logging.file")

        # Create logs directory if it doesn't exist
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # Remove existing handlers
        root_logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # File handler with rotation
        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
            )
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(log_format)
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)

        # Set third-party loggers to WARNING
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("werkzeug").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return LoggerSetup.setup(name)
