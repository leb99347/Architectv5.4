# strategies/time_based_exit.py

import datetime
import pytz

def should_exit_time_based(trade, context):
    """
    Exit positions before session close or weekend.
    Args:
        trade (dict): Trade info.
        context (dict): Market time info.
    Returns:
        dict: { "exit": bool, "reason": str }
    """
    timestamp = context.get("timestamp", datetime.datetime.now(pytz.UTC))
    weekday = timestamp.weekday()
    hour = timestamp.hour

    # Exit Friday evening or near known close times
    if (weekday == 4 and hour >= 20) or (weekday == 5):
        return {"exit": True, "reason": "session_close"}
    return {"exit": False}
