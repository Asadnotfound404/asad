import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Union


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
    """

    _configured_loggers: Dict[str, logging.Logger] = {}

    @staticmethod
    def get_logger(
        name: str,
        log_dir: str = "logs",
        log_file: str = "app.log",
        level: Optional[Union[int, str]] = None,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
        console: bool = True,
    ) -> logging.Logger:
        """
        Create or retrieve a configured logger.

        Parameters
        ----------
        name : str
            Logger name (usually __name__)
        log_dir : str
            Directory to store logs
        log_file : str
            Log filename
        level : int | str, optional
            Logging level (default: environment LOG_LEVEL or INFO)
        max_bytes : int
            Max size before rotation
        backup_count : int
            Number of backup files to retain
        console : bool
            Enable console logging

        Returns
        -------
        logging.Logger

        Example
        -------
        logger = LoggerFactory.get_logger(__name__)
        logger = LoggerFactory.get_logger(__name__, level="DEBUG")
        """

        # Resolve level
        if level is None:
            level_name = os.getenv("LOG_LEVEL", "INFO")
            level = getattr(logging, level_name.upper(), logging.INFO)

        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)

        # Return cached logger
        if name in LoggerFactory._configured_loggers:
            logger = LoggerFactory._configured_loggers[name]
            logger.setLevel(level)
            return logger

        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            file_path = os.path.join(log_dir, log_file)

            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            if console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

        LoggerFactory._configured_loggers[name] = logger
        return logger
