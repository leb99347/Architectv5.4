from indicators.pivot_zone_detector import detect_zones, confirm_multi_tap
from indicators.ema_filter import is_bullish_trend, is_bearish_trend
from indicators.doji_detector import is_doji
from indicators.atr_filter import compute_atr_ratio
from indicators.candles import is_strong_bullish, is_strong_bearish
from indicators.session_filter import is_session_active
from indicators.news_filter import should_block_trade
from ml.confidence_router import score_signal
from config.settings import CONFIDENCE_THRESHOLD


def generate_signal(data):
    # Safety check
    if not isinstance(data, dict) or "history" not in data:
        raise ValueError("generate_signal() requires a dict with a 'history' key containing past candles.")

    current = data
    history = data.get("history", [])
    price = current["close"]
    high = current["high"]
    low = current["low"]
    timestamp = current.get("timestamp")  # ISO8601 format

    # 🔒 News + Session Filter Block
    if should_block_trade():
        return _hold_signal(reason="news_blocked")
    if timestamp and not is_session_active(timestamp):
        return _hold_signal(reason="session_inactive")

    # 🔍 Zone Detection
    zones = detect_zones(history)
    zone_hit = any(abs(price - z) < 0.1 for z in zones)

    # 📈 Trend Filters
    bullish_trend = is_bullish_trend(current)
    bearish_trend = is_bearish_trend(current)

    # 🕯️ Candle Logic
    bullish_signal = zone_hit and is_strong_bullish(current) and bullish_trend
    bearish_signal = zone_hit and is_strong_bearish(current) and bearish_trend

    # 📌 Multi-Tap Score
    multi_tap_scores = [confirm_multi_tap(history, z) for z in zones]
    multi_tap_score = max(multi_tap_scores) if multi_tap_scores else 0.0

    # 📊 ATR Strength
    atr_ratio = compute_atr_ratio(history)

    # 🎯 Raw Feature Vector
    signal_dict = {
        "trend_alignment": int(bullish_trend if bullish_signal else bearish_trend),
        "breakout_strength": 1.0 if is_strong_bullish(current) or is_strong_bearish(current) else 0.3,
        "multi_tap_score": multi_tap_score,
        "atr_ratio": atr_ratio
    }

    # 🧠 ML Confidence + Tier Scoring
    preliminary_action = "buy" if bullish_signal else "sell" if bearish_signal else "hold"

    confidence = score_signal(signal_dict, model_id="4f")
    signal_dict["confidence"] = round(confidence, 3)
    signal_dict["selected_model"] = "4f"

    if confidence >= 0.85:
        tier = "A"
    elif confidence >= 0.70:
        tier = "B"
    elif confidence >= 0.50:
        tier = "C"
    else:
        tier = None

    signal_dict["tier"] = tier

    # ✅ Final trade decision logic
    if confidence >= CONFIDENCE_THRESHOLD and preliminary_action != "hold":
        action = preliminary_action
    else:
        action = "hold"

    return {
        "instrument": "GBP_JPY",
        "action": action,
        "confidence": signal_dict["confidence"],
        "tier": signal_dict["tier"],
        "tags": {
            "trend_alignment": signal_dict["trend_alignment"],
            "multi_tap_score": signal_dict["multi_tap_score"],
            "atr_ratio": signal_dict["atr_ratio"],
            "doji": is_doji(current),
            "ema_filter": bullish_trend or bearish_trend,
            "breakout_strength": signal_dict["breakout_strength"]
        },
        **signal_dict
    }


def _hold_signal(reason="hold"):
    return {
        "instrument": "GBP_JPY",
        "action": "hold",
        "confidence": None,
        "tier": None,
        "tags": {
            "reason": reason
        },
        "trend_alignment": 0,
        "breakout_strength": 0.0,
        "multi_tap_score": 0.0,
        "atr_ratio": 1.0
    }