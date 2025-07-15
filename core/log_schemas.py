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
        "result": trade.get("result", "unknown")  # win/loss/breakeven
    }
