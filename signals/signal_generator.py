# signals/signal_generator.py

from indicators.pivot_zone_detector import detect_zones, confirm_multi_tap
from indicators.ema_filter import is_bullish_trend, is_bearish_trend
from indicators.doji_detector import is_doji
from indicators.atr_filter import compute_atr_ratio
from indicators.candles import is_strong_bullish, is_strong_bearish
from indicators.news_filter import should_block_trade
from indicators.session_filter import is_session_active

import datetime
import pytz

def generate_signal(data):
    # Safety check
    if not isinstance(data, dict) or "history" not in data:
        raise ValueError("generate_signal() requires a dict with a 'history' key containing past candles.")

    current = data
    history = data.get("history", [])

    price = current["close"]
    high = current["high"]
    low = current["low"]

    # ✅ NEW: Check session logic
    from datetime import datetime
    import pytz
    candle_time = current.get("timestamp")
    candle_dt = datetime.fromisoformat(candle_time).astimezone(pytz.UTC) if candle_time else datetime.utcnow().astimezone(pytz.UTC)
    session_active = is_session_active(candle_dt)

    zones = detect_zones(history)
    zone_hit = any(abs(price - z) < 0.1 for z in zones)

    bullish_trend = is_bullish_trend(current)
    bearish_trend = is_bearish_trend(current)

    bullish_signal = zone_hit and is_strong_bullish(current) and bullish_trend
    bearish_signal = zone_hit and is_strong_bearish(current) and bearish_trend

    multi_tap_scores = [confirm_multi_tap(history, z) for z in zones]
    multi_tap_score = max(multi_tap_scores) if multi_tap_scores else 0.0

    atr_ratio = compute_atr_ratio(history)

    signal_dict = {
        "trend_alignment": int(bullish_trend if bullish_signal else bearish_trend),
        "breakout_strength": 1.0 if is_strong_bullish(current) or is_strong_bearish(current) else 0.3,
        "multi_tap_score": multi_tap_score,
        "atr_ratio": atr_ratio
    }

    if bullish_signal:
        action = "buy"
    elif bearish_signal:
        action = "sell"
    else:
        action = "hold"

    return {
        "instrument": "GBP_JPY",
        "action": action,
        "confidence": None,
        "tier": None,
        "tags": {
            "trend_alignment": signal_dict["trend_alignment"],
            "multi_tap_score": multi_tap_score,
            "atr_ratio": atr_ratio,
            "doji": is_doji(current),
            "ema_filter": bullish_trend or bearish_trend,
            "breakout_strength": signal_dict["breakout_strength"],
            "session_active": session_active  # ✅ <-- ADDED
        },
        **signal_dict
    }