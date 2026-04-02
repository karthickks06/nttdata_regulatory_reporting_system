"""Logging configuration for the application"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional

from app.core.config import settings


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    log_to_file: bool = True
) -> None:
    """
    Setup application logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        log_to_console: Whether to log to console
        log_to_file: Whether to log to file
    """
    level = getattr(logging, log_level or settings.LOG_LEVEL, logging.INFO)

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Setup handlers
    handlers = []

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(simple_formatter)
        handlers.append(console_handler)

    if log_to_file:
        # Create logs directory inside storage folder
        log_dir = Path(settings.STORAGE_PATH) / "logs" / "application"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Main application log with rotation
        file_path = log_file or str(log_dir / "app.log")
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        handlers.append(file_handler)

        # Error log - only errors and above
        error_file_handler = RotatingFileHandler(
            str(log_dir / "error.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(detailed_formatter)
        handlers.append(error_file_handler)

        # Daily rotating log
        daily_handler = TimedRotatingFileHandler(
            str(log_dir / "daily.log"),
            when='midnight',
            interval=1,
            backupCount=30,  # Keep 30 days
            encoding='utf-8'
        )
        daily_handler.setLevel(level)
        daily_handler.setFormatter(detailed_formatter)
        handlers.append(daily_handler)

    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True
    )

    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at level: {logging.getLevelName(level)}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter with additional context.

    Usage:
        logger = LoggerAdapter(logging.getLogger(__name__), {'request_id': '123'})
        logger.info('Processing request')
    """

    def process(self, msg, kwargs):
        """Add context to log messages"""
        if self.extra:
            context = ' | '.join(f'{k}={v}' for k, v in self.extra.items())
            msg = f'[{context}] {msg}'
        return msg, kwargs


def configure_agent_logging(agent_name: str) -> logging.Logger:
    """
    Configure logging for a specific agent.

    Args:
        agent_name: Name of the agent

    Returns:
        Logger instance for the agent
    """
    logger = logging.getLogger(f"agent.{agent_name}")

    # Create agent-specific log file inside storage folder
    log_dir = Path(settings.STORAGE_PATH) / "logs" / "agents"
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        str(log_dir / f"{agent_name}.log"),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger


def configure_audit_logging() -> logging.Logger:
    """
    Configure audit logging for security and compliance.

    Returns:
        Audit logger instance
    """
    audit_logger = logging.getLogger("audit")

    # Create audit log directory inside storage folder
    log_dir = Path(settings.STORAGE_PATH) / "logs" / "audit"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Audit logs should be append-only and never rotated by size
    # Use daily rotation for compliance
    handler = TimedRotatingFileHandler(
        str(log_dir / "audit.log"),
        when='midnight',
        interval=1,
        backupCount=365 * 7,  # Keep 7 years for compliance
        encoding='utf-8'
    )
    handler.setLevel(logging.INFO)

    # Audit log format
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.INFO)
    audit_logger.propagate = False  # Don't propagate to root logger

    return audit_logger


# Module-level logger
logger = logging.getLogger(__name__)

# Audit logger instance
audit_logger = configure_audit_logging()
