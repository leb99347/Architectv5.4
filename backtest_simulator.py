import os
import pandas as pd
from datetime import datetime
from signals.signal_generator import generate_signal
from strategies.exit_strategy import evaluate_exit_conditions
from indicators.news_filter import should_block_trade
from core.logger import log_trade
from core.shadow_logger import log_shadow_trade
from core.version_injector import attach_version
from indicators.session_filter import is_session_active
from config.settings import CONFIDENCE_THRESHOLD  # ✅ NEW

CSV_PATH = "data/sample_gbpjpy_ohlcv.csv"

def load_ohlcv_data(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df.sort_values("timestamp", inplace=True)

    # 🔧 Force numeric conversion
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    return df

def simulate_trades(df):
    win_count, loss_count, total_trades = 0, 0, 0
    blocked_count, low_conf_count = 0, 0

    for i in range(10, len(df)):
        if i % 100 == 0:
            print(f"📍 Progress: {i}/{len(df)}")
        history = df.iloc[i - 10:i].to_dict("records")
        current = df.iloc[i].to_dict()
        signal_time = current["timestamp"]

        signal_input = {
            **current,
            "history": history
        }

        # 🧱 Filter: Skip if news blocks
        if should_block_trade(signal_time):
            blocked_count += 1
            continue

        # 📡 Generate signal
        signal = generate_signal(signal_input)
        print(f"⛳ Signal @ {signal_time} → {signal}")

        direction = signal.get("action", "hold")
        confidence = signal.get("confidence")

        # 🚫 Skip if no confidence (e.g., session/news filtered)
        if confidence is None:
            continue

        # 🚫 Skip if below threshold
        if confidence < CONFIDENCE_THRESHOLD:
            print(f"⚠️ Skipping trade — confidence {confidence:.2f} < threshold {CONFIDENCE_THRESHOLD}")
            low_conf_count += 1
            continue

        if direction == "hold":
            continue

        # 🛠️ Simulate trade
        entry = current["close"]
        stop_loss = entry - 0.3 if direction == "buy" else entry + 0.3
        mock_trade = {
            "entry_price": entry,
            "side": direction,
            "stop_loss": stop_loss,
            "atr_multiplier": 1.5,
            "sl_buffer": 0.1,
            "drawdown_limit": 0.03,
            "trailing_type": "atr"
        }

        context = {
            "atr": 0.25,
            "volume": current.get("volume", 1000),
            "spread": 0.8,
            "time": signal_time
        }

        exit_decision = evaluate_exit_conditions(mock_trade, entry, context)
        # Simulate realistic ATR-based exit price
        if exit_decision["exit"]:
            exit_price = current["close"]
        else:
            simulated_move = 0.15 * (1 if direction == "buy" else -1)
            exit_price = entry + simulated_move

        pnl_pips = (exit_price - entry) * 100 if direction == "buy" else (entry - exit_price) * 100
        result = "win" if pnl_pips > 0 else "loss"
        total_trades += 1

        trade = {
            "timestamp": signal_time.isoformat(),
            "symbol": "GBPJPY",
            "direction": direction,
            "entry_price": round(entry, 3),
            "exit_price": round(exit_price, 3),
            "pnl_pips": round(pnl_pips, 1),
            "duration_min": 30,
            "confidence_f4": signal.get("confidence_f4"),
            "confidence_f10": signal.get("confidence_f10"),
            "model_used": signal.get("selected_model", "F4" if "confidence_f4" in signal else "unknown"),
            "confidence": confidence,
            "tier": signal.get("tier", None),
            "tags": {
                "trend_alignment": signal.get("trend_alignment", False),
                "breakout_strength": signal.get("breakout_strength", 0.0),
                "multi_tap_score": signal.get("multi_tap_score", 0.0),
                "atr_ratio": signal.get("atr_ratio", 1.0)
            },
            "exit_reason": exit_decision.get("reason", "manual_exit"),
            "was_news_blocked": False,
            "result": result
        }

        trade = attach_version(trade)
        log_trade(trade)
        log_shadow_trade(trade)

        if result == "win":
            win_count += 1
        else:
            loss_count += 1

    # 📊 Summary
    print(f"✅ Simulated {total_trades} trades → Wins: {win_count}, Losses: {loss_count}")
    print(f"🧼 Skipped due to low confidence: {low_conf_count}")
    print(f"🛑 Skipped due to news filter: {blocked_count}")
    print("📦 Logs written to `logs/trade_log.jsonl` and `logs/shadow_log.jsonl`")
    print("⏱️", signal_time, "→ session:", is_session_active(signal_time))


if __name__ == "__main__":
    df = load_ohlcv_data(CSV_PATH)
    simulate_trades(df)