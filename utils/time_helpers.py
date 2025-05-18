import time

# This module provides helper functions
# ----------------------------------------------------
# Time and date utilities

def get_unix_time():
    """Returns the UNIX time in seconds (since Jan 1, 1970)."""
    return time.time() + 946684800  # Offset between 2000 and 1970 in seconds

def get_local_time(timezone):
    """
    Returns local time with a manual offset in seconds.
    Default is +2 hours for Central European Summer Time (CEST).
    """
    offset = timezone * 3600
    return time.localtime(time.time() + offset)

def format_timestamp(ts=None):
    """
    Formats a time tuple (e.g. from time.localtime()) into a readable string.
    If no time is given, uses current local time with default offset.
    """
    if ts is None:
        ts = get_local_time(2)
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(*ts[:6])