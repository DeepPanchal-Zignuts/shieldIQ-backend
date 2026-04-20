"""
Date & time utility functions.
Centralized location for time operations to ensure consistency (UTC epoch milliseconds).
"""

from datetime import datetime, timezone as dt_timezone
from django.utils import timezone


def get_now() -> datetime:
    """Return the current timezone-aware datetime in UTC."""
    return timezone.now()


def get_current_timestamp_ms() -> int:
    """Return current UTC epoch timestamp in milliseconds."""
    return int(timezone.now().timestamp() * 1000)


def datetime_to_timestamp_ms(dt: datetime) -> int:
    """Convert a datetime object to UTC epoch timestamp in milliseconds."""
    if not dt:
        return 0
    # Ensure it's aware, if not assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dt_timezone.utc)
    return int(dt.timestamp() * 1000)


def timestamp_ms_to_datetime(ts_ms: int) -> datetime:
    """Convert UTC epoch timestamp in milliseconds to a timezone-aware datetime object."""
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=dt_timezone.utc)


def now() -> datetime:
    """Legacy wrapper for get_now."""
    return get_now()


def utc_now() -> datetime:
    """Legacy wrapper for get_now."""
    return get_now()


def add_minutes(dt: datetime = None, minutes: int = 0) -> datetime:
    """Add N minutes to a datetime (defaults to now)."""
    from datetime import timedelta

    base = dt or get_now()
    return base + timedelta(minutes=minutes)


def add_hours(dt: datetime = None, hours: int = 0) -> datetime:
    """Add N hours to a datetime (defaults to now)."""
    from datetime import timedelta

    base = dt or get_now()
    return base + timedelta(hours=hours)


def add_days(dt: datetime = None, days: int = 0) -> datetime:
    """Add N days to a datetime (defaults to now)."""
    from datetime import timedelta

    base = dt or get_now()
    return base + timedelta(days=days)


def is_expired(expiry_dt: datetime) -> bool:
    """Check if a datetime is in the past."""
    return expiry_dt < get_now()


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%S%z") -> str:
    """Format a datetime to string."""
    return dt.strftime(fmt)


def parse_datetime(date_string: str, fmt: str = "%Y-%m-%dT%H:%M:%S%z") -> datetime:
    """Parse a string to a timezone-aware datetime."""
    return datetime.strptime(date_string, fmt)


def get_current_date():
    """Return the current date (UTC) without time."""
    return get_now().date()
