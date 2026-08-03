"""
Shared custom exceptions for the AQI Forecast & Environmental Analytics
Platform.

Centralized here so every layer raises and catches consistent, specific
exception types instead of bare `Exception` (Handbook Section 8.11,
Error Handling Standards).
"""


class AQIPlatformError(Exception):
    """Base class for all custom exceptions raised by this project."""


class DatasetLoadError(AQIPlatformError):
    """Raised when a dataset file cannot be located, read, or parsed."""


class DatasetValidationError(AQIPlatformError):
    """Raised when a loaded dataset fails required-column or integrity checks."""
