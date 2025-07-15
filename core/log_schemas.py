# core/log_schemas.py

def format_trade_log(trade):
    return {
        "timestamp": trade.get("timestamp"),
        "symbol": trade.get("symbol", "GBPJPY"),
        "direction": trade.get("direction"),
        "entry_price": trade.get("entry_price"),
        "exit_price": trade.get("exit_price"),
        "pnl_pips": trade.get("pnl_pips"),
        "duration_min": trade.get("duration_min"),
        "confidence": trade.get("confidence"),
        "tier": trade.get("tier"),
        "tags": trade.get("tags", {}),
        "result": trade.get("result", "unknown"),
        "exit_reason": trade.get("exit_reason", "unspecified"),
        "strategy_version": trade.get("strategy_version", "v5.4"),
        "exit_metadata": trade.get("exit_metadata", {})  # Optional details like trailing SL, drawdown, etc.
    }