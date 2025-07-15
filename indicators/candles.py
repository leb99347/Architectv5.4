# indicators/candles.py

def is_strong_bullish(candle, threshold=0.6):
    body = candle["close"] - candle["open"]
    range_ = candle["high"] - candle["low"]
    return body > 0 and body / range_ > threshold if range_ > 0 else False

def is_strong_bearish(candle, threshold=0.6):
    body = candle["open"] - candle["close"]
    range_ = candle["high"] - candle["low"]
    return body > 0 and body / range_ > threshold if range_ > 0 else False
