"""
Application-wide settings for the AQI Forecast & Environmental
Analytics Platform.

Import from this module instead of hardcoding configuration values
inside business logic (Master Development Handbook Section 5.8).
"""

PROJECT_NAME = "AQI Forecast & Environmental Analytics Platform"
PROJECT_VERSION = "0.1.0"

# Logging (Handbook Section 8.12)
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# Dashboard (NFR-PERF-001/002, UI-NAV-001)
DASHBOARD_PAGE_TITLE = "AQI Forecast & Environmental Analytics"
DASHBOARD_LAYOUT = "wide"
DASHBOARD_STARTUP_TIMEOUT_SECONDS = 10
