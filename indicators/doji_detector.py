# indicators/doji_detector.py

def is_doji(candle: dict, threshold: float = 0.1) -> bool:
    body = abs(candle['close'] - candle['open'])
    range_ = candle['high'] - candle['low']
    return body / range_ < threshold if range_ > 0 else False
