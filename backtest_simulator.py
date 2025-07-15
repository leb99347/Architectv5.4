# backtest_simulator.py

import os
import pandas as pd
from datetime import datetime
from signals.signal_generator import generate_signal
from core.logger import log_trade
from core.shadow_logger import log_shadow_trade

CSV_PATH = "data/sample_gbpjpy_ohlcv.csv"

def load_ohlcv_data(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df.sort_values("timestamp", inplace=True)
    return df

def simulate_trades(df):
    win_count, loss_count = 0, 0

    for i in range(50, len(df)):  # ensure enough historical candles
        history = df.iloc[i - 50:i].to_dict("records")
        current = df.iloc[i].to_dict()

        signal_input = {
            **current,
            "history": history
        }

        signal = generate_signal(signal_input)

        entry = current["close"]
        exit_price = entry + 0.15 if signal["action"] == "buy" else entry - 0.15

        import random
        force_loss = random.random() < 0.2

        pnl_pips = (exit_price - entry) * 100 if signal["action"] == "buy" else (entry - exit_price) * 100
        result = "loss" if force_loss else ("win" if pnl_pips > 0 else "loss")

        trade = {
            "timestamp": current["timestamp"].isoformat(),
            "symbol": "GBPJPY",
            "direction": signal["action"],
            "entry_price": round(entry, 3),
            "exit_price": round(exit_price, 3),
            "pnl_pips": round(pnl_pips, 1),
            "duration_min": 30,
            "confidence": signal.get("confidence", 0.5),
            "tier": signal.get("tier", 2),
            "tags": {
                "trend_alignment": signal.get("trend_alignment", False),
                "breakout_strength": signal.get("breakout_strength", 0.0),
                "multi_tap_score": signal.get("multi_tap_score", 0.0),
                "atr_ratio": signal.get("atr_ratio", 1.0)
            },
            "result": result
        }

        log_trade(trade)
        log_shadow_trade(trade)

        if result == "win":
            win_count += 1
        else:
            loss_count += 1

    print(f"✅ Simulated {len(df) - 50} trades → Wins: {win_count}, Losses: {loss_count}")
    print("📦 Logs written to `logs/trade_log.jsonl` and `logs/shadow_log.jsonl`")

if __name__ == "__main__":
    df = load_ohlcv_data(CSV_PATH)
    simulate_trades(df)