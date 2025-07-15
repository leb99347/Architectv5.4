def detect_zones(candles: list, lookback: int = 50, tolerance: float = 0.1) -> list:
    zones = []
    for i in range(2, lookback - 2):
        high = candles[i]["high"]
        low = candles[i]["low"]

        if high > candles[i - 1]["high"] and high > candles[i + 1]["high"]:
            zones.append(round(high, 3))  # Resistance

        if low < candles[i - 1]["low"] and low < candles[i + 1]["low"]:
            zones.append(round(low, 3))  # Support

    return sorted(set(zones))


def confirm_multi_tap(candles: list, zone: float, tolerance: float = 0.1) -> float:
    taps = 0
    for candle in candles:
        if abs(candle["high"] - zone) <= tolerance or abs(candle["low"] - zone) <= tolerance:
            taps += 1

    return min(taps / 3, 1.0)  # Normalized to [0.0, 1.0]
