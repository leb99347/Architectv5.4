# signals/signal_generator.py

from indicators.pivot_zone_detector import detect_zones, confirm_multi_tap
from indicators.ema_filter import is_bullish_trend, is_bearish_trend
from indicators.doji_detector import is_doji
from indicators.atr_filter import compute_atr_ratio
from indicators.candles import is_strong_bullish, is_strong_bearish


def generate_signal(data):
    # Safety check
    if not isinstance(data, dict) or "history" not in data:
        raise ValueError("generate_signal() requires a dict with a 'history' key containing past candles.")

    # Use most recent candle for single-point logic
    current = data
    history = data.get("history", [])  # list of past candles

    # Extract core price info
    price = current["close"]
    high = current["high"]
    low = current["low"]

    # Detect pivot zones from historical structure
    zones = detect_zones(history)
    zone_hit = any(abs(price - z) < 0.1 for z in zones)

    # Trend filter (based on higher timeframe EMA)
    bullish_trend = is_bullish_trend(current)
    bearish_trend = is_bearish_trend(current)

    # Candle strength confirmation
    bullish_signal = zone_hit and is_strong_bullish(current) and bullish_trend
    bearish_signal = zone_hit and is_strong_bearish(current) and bearish_trend

    # Multi-tap scoring from historical candles
    # Multi-tap scoring from historical candles
    multi_tap_scores = [confirm_multi_tap(history, z) for z in zones]
    multi_tap_score = max(multi_tap_scores) if multi_tap_scores else 0.0

    # ATR breakout strength (based on recent volatility)
    atr_ratio = compute_atr_ratio(history)

    # Raw ML feature input
    signal_dict = {
        "trend_alignment": int(bullish_trend if bullish_signal else bearish_trend),
        "breakout_strength": 1.0 if is_strong_bullish(current) or is_strong_bearish(current) else 0.3,
        "multi_tap_score": multi_tap_score,
        "atr_ratio": atr_ratio
    }

    # Final trading decision
    if bullish_signal:
        action = "buy"
    elif bearish_signal:
        action = "sell"
    else:
        action = "hold"

    return {
        "instrument": "GBP_JPY",
        "action": action,
        "confidence": None,  # populated by confidence model later
        "tier": None,
        "tags": {
            "trend_alignment": signal_dict["trend_alignment"],
            "multi_tap_score": multi_tap_score,
            "atr_ratio": atr_ratio,
            "doji": is_doji(current),
            "ema_filter": bullish_trend or bearish_trend,
            "breakout_strength": signal_dict["breakout_strength"]
        },
        **signal_dict
    }