# strategies/consolidation_exit.py

def should_exit_consolidation(trade, context):
    """
    Exit if price remains stagnant for too long after entry.
    Args:
        trade (dict): Contains entry time, etc.
        context (dict): Includes current time, volatility score, etc.
    Returns:
        dict: { "exit": bool, "reason": str }
    """
    max_hold_minutes = trade.get("max_consolidation_minutes", 90)
    entry_time = trade.get("entry_time")
    current_time = context.get("timestamp")
    if not entry_time or not current_time:
        return {"exit": False}

    elapsed = (current_time - entry_time).total_seconds() / 60.0
    if elapsed >= max_hold_minutes and context.get("volatility_score", 1.0) < 0.3:
        return {"exit": True, "reason": "consolidation_timeout"}
    return {"exit": False}
