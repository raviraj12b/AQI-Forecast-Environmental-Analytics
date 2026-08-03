"""
Centralized logging configuration (Handbook Section 8.12, Logging Standards).

Modules should call `get_logger(__name__)` rather than using `print()`.
"""

import logging

from config.settings import LOG_FORMAT, LOG_LEVEL

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger for `name`.

    The root logger is configured exactly once per process, using the
    level/format defined in `config.settings`.
    """
    global _CONFIGURED
    if not _CONFIGURED:
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL, logging.INFO), format=LOG_FORMAT
        )
        _CONFIGURED = True
    return logging.getLogger(name)
