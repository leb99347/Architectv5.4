# app.py

import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from signals.signal_generator import generate_signal
from strategies.exit_strategy import evaluate_exit_conditions
from ml.confidence_model_live import live_score
from core.logger import log_trade
from core.shadow_logger import log_shadow_trade
from core.version_injector import attach_version
from core.logging import log_event
from core.trade_executor import execute_trade

# Optional: Enable this if you want VS Code logs
logging.basicConfig(level=logging.INFO)

load_dotenv()

def fetch_live_market_data():
    # Placeholder: Replace this with your OANDA or other live API call
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "open": 154.5,
        "high": 155.0,
        "low": 154.2,
        "close": 154.8,
        "volume": 1200,
        "history": []  # Populate with real historical candles
    }

def main():
    print("🚀 Running ArchitectV4 Live Trading Loop")

    market_data = fetch_live_market_data()
    signal = generate_signal(market_data)

    if signal.get("action", "hold") == "hold":
        print("🟡 No trade signal at this time.")
        return

    signal["confidence"] = live_score(signal)

    # Build trade dictionary
    trade = {
        "timestamp": market_data["timestamp"],
        "symbol": "GBPJPY",
        "direction": signal["action"],
        "entry_price": market_data["close"],
        "confidence": signal["confidence"],
        "tier": signal.get("tier", 2),
        "tags": {
            "trend_alignment": signal.get("trend_alignment", False),
            "breakout_strength": signal.get("breakout_strength", 0.0),
            "multi_tap_score": signal.get("multi_tap_score", 0.0),
            "atr_ratio": signal.get("atr_ratio", 1.0)
        }
    }

    # Evaluate and simulate exit (in live: you'd place order and track live PnL)
    context = {
        "atr": 0.25,
        "volume": market_data.get("volume", 1000),
        "spread": 0.8,
        "time": market_data["timestamp"]
    }

    # Dummy values for now — replace in live implementation
    trade["stop_loss"] = trade["entry_price"] - 0.3 if trade["direction"] == "buy" else trade["entry_price"] + 0.3
    exit_info = evaluate_exit_conditions(trade, trade["entry_price"], context)
    trade["exit_reason"] = exit_info.get("reason", "manual_exit")
    trade["exit_price"] = trade["entry_price"] + 0.15 if trade["direction"] == "buy" else trade["entry_price"] - 0.15
    trade["pnl_pips"] = round((trade["exit_price"] - trade["entry_price"]) * 100, 1) if trade["direction"] == "buy" else round((trade["entry_price"] - trade["exit_price"]) * 100, 1)
    trade["duration_min"] = 30
    trade["result"] = "win" if trade["pnl_pips"] > 0 else "loss"
    trade["was_news_blocked"] = False

    # Ensure version and feature tagging
    trade = attach_version(trade)

    # ✅ Execute trade (logs both primary and shadow + event trail)
    execute_trade(trade)

if __name__ == "__main__":
    main()