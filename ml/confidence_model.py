"""
confidence_model.py — Scores trade signals based on rules or ML models.
"""

import numpy as np
import logging
from config.settings import CONFIDENCE_THRESHOLD

def score_signal(signal):
    """
    Compute a confidence score (0.0 to 1.0) for a given signal.

    Inputs (example signal dict):
    {
        'direction': 'buy',
        'breakout_strength': 0.8,
        'trend_alignment': True,
        'multi_tap_score': 0.7,
        'atr_ratio': 1.2
    }
    """
    score = 0.0

    # Rule-based weighting system (adjust as needed)
    if signal.get('trend_alignment'):
        score += 0.3
    score += 0.3 * signal.get('breakout_strength', 0)
    score += 0.2 * signal.get('multi_tap_score', 0)
    atr_ratio = signal.get('atr_ratio', 1)
    score += 0.2 * min(1.0, atr_ratio / 2)

    final_score = round(min(score, 1.0), 3)
    logging.info(f"[CONFIDENCE] Signal scored: {final_score}")
    return final_score

def is_confident(signal):
    return score_signal(signal) >= CONFIDENCE_THRESHOLD
