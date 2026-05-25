"""
Logging configuration for Realtor Agent system.
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Optional

import structlog


def setup_logging(level: str = "INFO", log_file: Optional[str] = None, json_format: bool = False) -> None:
    """
    Setup structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        json_format: Whether to use JSON format for logs
    """
    # Configure standard library logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
            "detailed": {"format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "standard" if not json_format else "json",
                "stream": sys.stdout,
            },
        },
        "root": {
            "level": level,
            "handlers": ["console"],
        },
        "loggers": {
            "realtor_agent": {
                "level": level,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "fastapi": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    # Add file handler if specified
    if log_file:
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        logging_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": level,
            "formatter": "detailed",
            "filename": str(log_file_path),
        }

        # Add file handler to all loggers
        for logger_config in logging_config["loggers"].values():
            logger_config["handlers"].append("file")
        logging_config["root"]["handlers"].append("file")

    # Apply logging configuration
    logging.config.dictConfig(logging_config)

    # Configure structlog
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if json_format:
        # JSON logging for production
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        # Human-readable logging for development
        shared_processors.append(
            structlog.dev.ConsoleRenderer(
                colors={
                    "timestamp": "green",
                    "level": "bold_red",
                    "logger": "blue",
                    "event": "reset",
                }
            )
        )

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class to add logging to any class."""

    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class."""
        return get_logger(self.__class__.__module__ + "." + self.__class__.__name__)
