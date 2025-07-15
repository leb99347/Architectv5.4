# indicators/session_filter.py

from datetime import datetime

def is_in_session(timestamp: str) -> bool:
    hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").hour
    return 6 <= hour <= 15  # London–New York overlap (10AM–3PM UTC)
