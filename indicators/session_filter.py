# indicators/session_filter.py

import datetime
import pytz
from dateutil import parser  # ← Use this for flexible ISO parsing

LONDON_START = datetime.time(7, 0)
LONDON_END = datetime.time(16, 0)
NY_START = datetime.time(12, 0)
NY_END = datetime.time(21, 0)

def is_session_active(timestamp_input) -> bool:
    """
    Check if timestamp is within London or NY session (UTC).
    Accepts ISO string or datetime object (tz-aware or tz-naive).
    """
    try:
        # Parse string if needed
        if isinstance(timestamp_input, str):
            dt = parser.isoparse(timestamp_input)
        else:
            dt = timestamp_input

        # Localize if tz-naive, else convert to UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        else:
            dt = dt.astimezone(pytz.UTC)

        time_only = dt.time()
        return (LONDON_START <= time_only <= LONDON_END) or (NY_START <= time_only <= NY_END)
    except Exception as e:
        print(f"⚠️ Session check failed: {e}")
        return False