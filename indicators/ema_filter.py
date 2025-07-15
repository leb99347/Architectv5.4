# indicators/ema_filter.py

import pandas as pd

def ema_trend_filter(df: pd.DataFrame, period: int = 50) -> str:
    df['EMA'] = df['close'].ewm(span=period, adjust=False).mean()
    latest_price = df['close'].iloc[-1]
    latest_ema = df['EMA'].iloc[-1]

    if latest_price > latest_ema:
        return 'bullish'
    elif latest_price < latest_ema:
        return 'bearish'
    else:
        return 'neutral'

def is_bullish_trend(data: dict) -> bool:
    return data.get("trend") == "bullish"

def is_bearish_trend(data: dict) -> bool:
    return data.get("trend") == "bearish"
