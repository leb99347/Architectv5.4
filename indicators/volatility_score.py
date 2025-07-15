def volatility_score(atr: float, threshold: float = 0.5) -> bool:
    return atr > threshold
