def detect_zones(candles):
    zones = []
    for i in range(1, len(candles) - 1):
        low = float(candles[i]["low"])
        high = float(candles[i]["high"])
        if low < float(candles[i - 1]["low"]) and low < float(candles[i + 1]["low"]):
            zones.append(round(low, 3))  # Support
        elif high > float(candles[i - 1]["high"]) and high > float(candles[i + 1]["high"]):
            zones.append(round(high, 3))  # Resistance
    return zones


def confirm_multi_tap(candles: list, zone: float, tolerance: float = 0.1) -> float:
    taps = 0
    for candle in candles:
        if abs(candle["high"] - zone) <= tolerance or abs(candle["low"] - zone) <= tolerance:
            taps += 1

    return min(taps / 3, 1.0)  # Normalized to [0.0, 1.0]
