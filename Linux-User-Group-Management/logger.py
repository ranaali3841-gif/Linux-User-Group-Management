"""Logging architecture for auditing and historical metrics tracking."""

import logging
import sys
from config import LOG_DIR

def setup_logger(name: str = "system_admin") -> logging.Logger:
    """Configures and provisions a high-reliability system audit logger.

    Args:
        name (str): Unique identity context name for isolating logged runs.

    Returns:
        logging.Logger: System configured infrastructure audit logger instance.
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File Handler
    file_handler = logging.FileHandler(LOG_DIR / "audit.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()