import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Union
import json


class JsonFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    Useful for cloud / monitoring systems.
    """

    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


class LoggerFactory:
    """
    Production-grade Logger Factory.

    Features:
    - Rotating file handler
    - Optional console handler
    - Environment-based log level
    - Duplicate handler protection
    - Safe caching
    - UTF-8 encoding
    - Optional JSON logging
    """

    _configured_loggers: Dict[str, logging.Logger] = {}

    @staticmethod
    def get_logger(
        name: str,
        log_dir: str = "logs",
        log_file: Optional[str] = None,
        level: Optional[Union[int, str]] = None,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
        console: bool = True,
        json_format: bool = False,
    ) -> logging.Logger:

        # Resolve logging level
        if level is None:
            level_name = os.getenv("LOG_LEVEL", "INFO")
            level = getattr(logging, level_name.upper(), logging.INFO)

        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)

        # Return cached logger if exists
        if name in LoggerFactory._configured_loggers:
            logger = LoggerFactory._configured_loggers[name]
            logger.setLevel(level)
            return logger

        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        if not logger.handlers:

            # Default log file name per module
            if log_file is None:
                log_file = f"{name}.log"

            file_path = os.path.join(log_dir, log_file)

            # Choose formatter
            if json_format:
                formatter = JsonFormatter()
            else:
                formatter = logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                )

            # File handler
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # Console handler
            if console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

        LoggerFactory._configured_loggers[name] = logger
        return logger
