# strategies/max_drawdown.py

def should_exit_drawdown(trade, current_price, context):
    """
    Exit if the trade exceeds a maximum allowed drawdown.

    Args:
        trade (dict): Should contain 'entry_price', 'side', and optionally 'drawdown_limit'
        current_price (float): Current market price
        context (dict): Reserved for future market metadata or enhancements

    Returns:
        dict: {
            'exit': bool,
            'reason': str (if exit triggered),
            'drawdown': float (optional)
        }
    """
    threshold = trade.get("drawdown_limit", 0.03)  # 3% default max drawdown
    entry_price = trade.get("entry_price")
    side = trade.get("side", "buy")

    if not entry_price:
        return {"exit": False, "reason": "missing_entry_price"}

    # Calculate drawdown
    if side == "buy":
        drawdown = (entry_price - current_price) / entry_price
    else:  # sell
        drawdown = (current_price - entry_price) / entry_price

    if drawdown > threshold:
        return {"exit": True, "reason": "max_drawdown", "drawdown": round(drawdown, 4)}

    return {"exit": False, "reason": "drawdown_within_limit", "drawdown": round(drawdown, 4)}