# strategies/liquidity_filter.py

def is_liquidity_thin(context):
    """
    Determines if current market conditions indicate low liquidity.

    Args:
        context (dict): Contains market metadata such as 'spread', 'volume', 'time', etc.

    Returns:
        bool: True if liquidity is considered too thin for reliable trading.
    """
    spread = context.get("spread")  # In pips or price units
    volume = context.get("volume")  # Tick or contract volume
    time = context.get("time")      # datetime object or session label

    # Example conditions — these can be expanded over time
    if spread is not None and spread > 0.0008:
        return True  # Spread too wide

    if volume is not None and volume < 100:  # Arbitrary low volume threshold
        return True

    if isinstance(time, str) and time.lower() in ["asia_preopen", "late_friday"]:
        return True  # Custom low-liquidity times

    return False