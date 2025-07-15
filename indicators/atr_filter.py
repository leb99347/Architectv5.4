# indicators/atr_filter.py

import pandas as pd

def atr_filter(df: pd.DataFrame, period: int = 14) -> float:
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df['ATR'].iloc[-1]

def compute_atr_ratio(history: list, period: int = 14, baseline_atr: float = 0.15) -> float:
    if not history or len(history) < period + 1:
        return 1.0  # Fallback value if not enough data

    try:
        highs = [candle["high"] for candle in history[-period:]]
        lows = [candle["low"] for candle in history[-period:]]
        closes = [candle["close"] for candle in history[-(period + 1):-1]]

        trs = []
        for i in range(period):
            hl = highs[i] - lows[i]
            hpc = abs(highs[i] - closes[i])
            lpc = abs(lows[i] - closes[i])
            trs.append(max(hl, hpc, lpc))

        atr = sum(trs) / len(trs)
        latest_range = history[-1]["high"] - history[-1]["low"]
        return round(min(latest_range / atr, 2.0), 3) if atr else 1.0

    except Exception as e:
        print(f"[ATR Filter] Error computing ATR ratio: {e}")
        return 1.0
