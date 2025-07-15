# strategies/exit_strategy.py

from strategies.trailing_stop import should_exit_trailing
from strategies.max_drawdown import should_exit_drawdown
from strategies.liquidity_filter import is_liquidity_thin
from strategies.time_based_exit import should_exit_time_based
from strategies.signal_override import should_exit_signal_override
from strategies.consolidation_exit import should_exit_consolidation
from indicators.news_filter import should_block_trade  # Optional but active

def evaluate_exit_conditions(trade, current_price, context):
    """
    Centralized exit condition handler for live/shadow/backtest environments.
    """

    # 🟢 Trailing Stop
    trailing_result = should_exit_trailing(trade, current_price, context)
    if trailing_result.get("exit"):
        return {
            "exit": True,
            "reason": trailing_result.get("reason", "trailing_stop"),
            "new_sl": trailing_result.get("new_sl")
        }

    # 🔴 Max Drawdown
    drawdown_result = should_exit_drawdown(trade, current_price, context)
    if drawdown_result.get("exit"):
        return {
            "exit": True,
            "reason": drawdown_result.get("reason", "max_drawdown")
        }

    # ⚠️ Liquidity Filter
    if is_liquidity_thin(context):
        return {"exit": True, "reason": "thin_liquidity"}

    # ⏱️ Time-Based Exit (e.g., session close, weekends)
    time_exit = should_exit_time_based(trade, context)
    if time_exit.get("exit"):
        return time_exit

    # 🔁 Signal Override (if new signal contradicts active trade)
    override_exit = should_exit_signal_override(trade, context)
    if override_exit.get("exit"):
        return override_exit

    # 💤 Consolidation Timeout (flat market, time decay)
    flat_exit = should_exit_consolidation(trade, context)
    if flat_exit.get("exit"):
        return flat_exit

    # 🚨 Optional: News Event Filter (exit near high-impact event)
    if should_block_trade(context.get("timestamp")):
        return {"exit": True, "reason": "news_event_proximity"}

    # ✅ No exit triggered
    return {"exit": False, "reason": "hold"}