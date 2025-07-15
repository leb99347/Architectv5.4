# strategies/trailing_stop.py

def should_exit_trailing(trade, current_price, context):
    """
    Determines whether to exit the trade based on a trailing stop strategy.

    Args:
        trade (dict): {
            'entry_price': float,
            'side': 'buy' or 'sell',
            'stop_loss': float,
            'trailing_type': 'atr' or 'fixed',
            'sl_buffer': float,
            'atr_multiplier': float,
            'fixed_sl_buffer': float
        }
        current_price (float): Latest price
        context (dict): {
            'atr': float (optional),
            ...
        }

    Returns:
        dict: {
            'exit': bool,
            'reason': str,
            'new_sl': float (optional)
        }
    """
    entry_price = trade.get("entry_price")
    stop_loss = trade.get("stop_loss", entry_price)
    side = trade.get("side", "buy")
    trailing_type = trade.get("trailing_type", "atr")

    atr = context.get("atr")
    atr_multiplier = trade.get("atr_multiplier", 1.5)
    sl_buffer = trade.get("sl_buffer", 0.2)  # Prevents noise-based triggers
    fixed_buffer = trade.get("fixed_sl_buffer", 0.0015)

    # --- ATR-Based Trailing ---
    if trailing_type == "atr" and atr:
        if side == "buy":
            dynamic_sl = max(stop_loss, current_price - (atr * atr_multiplier))
            if current_price <= dynamic_sl + sl_buffer:
                return {
                    "exit": True,
                    "reason": "atr_trailing_stop",
                    "new_sl": dynamic_sl
                }
            elif dynamic_sl > stop_loss:
                return {
                    "exit": False,
                    "reason": "trailing_adjust",
                    "new_sl": dynamic_sl
                }

        elif side == "sell":
            dynamic_sl = min(stop_loss, current_price + (atr * atr_multiplier))
            if current_price >= dynamic_sl - sl_buffer:
                return {
                    "exit": True,
                    "reason": "atr_trailing_stop",
                    "new_sl": dynamic_sl
                }
            elif dynamic_sl < stop_loss:
                return {
                    "exit": False,
                    "reason": "trailing_adjust",
                    "new_sl": dynamic_sl
                }

    # --- Fixed Trailing (Fallback) ---
    else:
        if side == "buy" and current_price <= stop_loss + fixed_buffer:
            return {"exit": True, "reason": "fixed_trailing_stop"}
        elif side == "sell" and current_price >= stop_loss - fixed_buffer:
            return {"exit": True, "reason": "fixed_trailing_stop"}

    return {"exit": False, "reason": "hold"}