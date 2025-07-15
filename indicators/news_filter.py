import json
import os
import datetime
from dateutil import parser as dtparser
import pytz
import logging

# Paths (adjust as needed)
MOCK_NEWS_PATH = "data/news_events.json"  # Fallback for backtesting
FILTER_ENABLED = True
NEWS_LOOKAHEAD_MINUTES = 15  # Look X min forward for high-impact events

def _load_mock_news():
    if not os.path.exists(MOCK_NEWS_PATH):
        logging.warning("[NewsFilter] No mock news file found.")
        return []
    with open(MOCK_NEWS_PATH, "r") as f:
        return json.load(f)

def _now_utc():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

def _parse_datetime_safe(value):
    """Ensure signal_time is timezone-aware datetime."""
    try:
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                return value.tz_localize(pytz.UTC)  # ⛑ safe for pandas.Timestamp too
            else:
                return value.astimezone(pytz.UTC)
        return dtparser.parse(value).astimezone(pytz.UTC)
    except Exception as e:
        logging.error(f"[NewsFilter] Failed to parse datetime: {value} ({e})")
        return _now_utc()  # fallback

def should_block_trade(signal_time=None, impact_level="high"):
    """
    Returns True if a high-impact event is within ±NEWS_LOOKAHEAD_MINUTES of signal_time (UTC).
    signal_time: datetime or ISO8601 string (default: now)
    """
    if not FILTER_ENABLED:
        return False

    signal_time = _parse_datetime_safe(signal_time or _now_utc())
    news_data = _load_mock_news()

    for event in news_data:
        if event.get("impact", "").lower() != impact_level:
            continue
        try:
            event_time = dtparser.parse(event["time"]).astimezone(pytz.UTC)
            delta = abs((event_time - signal_time).total_seconds()) / 60.0
            if delta <= NEWS_LOOKAHEAD_MINUTES:
                logging.info(f"[NewsFilter] Blocking trade due to nearby event: {event['title']} @ {event_time}")
                return True
        except Exception as e:
            logging.warning(f"[NewsFilter] Failed to parse event time: {event} ({e})")
            continue

    return False