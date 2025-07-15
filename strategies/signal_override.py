# strategies/signal_override.py

def should_exit_signal_override(trade, context):
    """
    Exit if new signal contradicts the direction of the current trade.
    Args:
        trade (dict): Contains 'side' (buy/sell).
        context (dict): Includes 'latest_signal' (buy/sell/hold).
    Returns:
        dict: { "exit": bool, "reason": str }
    """
    signal = context.get("latest_signal")
    if not signal:
        return {"exit": False}

    side = trade.get("side")
    if (side == "buy" and signal == "sell") or (side == "sell" and signal == "buy"):
        return {"exit": True, "reason": "signal_override"}

    return {"exit": False}
