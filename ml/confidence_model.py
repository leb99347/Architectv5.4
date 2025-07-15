"""
confidence_model.py — Scores trade signals based on rules or trained ML models.
"""

import numpy as np
import logging
import os
import joblib
from config.settings import CONFIDENCE_THRESHOLD

MODEL_PATH = "ml/confidence_model.pkl"

# --------------------------
# Rule-Based Scoring Logic
# --------------------------
def rule_based_score(signal):
    """
    Compute a confidence score (0.0 to 1.0) for a given signal using static weights.
    """
    score = 0.0
    if signal.get('trend_alignment'):
        score += 0.3
    score += 0.3 * signal.get('breakout_strength', 0)
    score += 0.2 * signal.get('multi_tap_score', 0)
    atr_ratio = signal.get('atr_ratio', 1)
    score += 0.2 * min(1.0, atr_ratio / 2)
    final_score = round(min(score, 1.0), 3)
    logging.info(f"[CONFIDENCE][Rule] Score: {final_score}")
    return final_score

# --------------------------
# ML-Based Scoring Logic
# --------------------------
def model_based_score(signal):
    """
    Uses trained model to compute a confidence score based on learned patterns.
    """
    if not os.path.exists(MODEL_PATH):
        logging.warning("[CONFIDENCE] Model not found, falling back to rule-based.")
        return rule_based_score(signal)

    try:
        model = joblib.load(MODEL_PATH)
        feature_vector = [
            float(signal.get("doji", 0)),
            float(signal.get("ema_filter", 0)),
            float(signal.get("atr_filter", 0)),
            float(signal.get("session_filter", 0)),
            float(signal.get("pivot_zone", 0)),
            float(signal.get("volatility_score", 0)),
            float(signal.get("breakout_strength", 0)),
            float(signal.get("zone_tap_count", 1)),
        ]
        proba = model.predict_proba([feature_vector])[0][1]
        final_score = round(proba, 3)
        logging.info(f"[CONFIDENCE][Model] Score: {final_score}")
        return final_score
    except Exception as e:
        logging.error(f"[CONFIDENCE] Model scoring error: {e}")
        return rule_based_score(signal)

# --------------------------
# Unified Confidence Scoring API
# --------------------------
def get_confidence_score(signal):
    return model_based_score(signal)

def is_confident(signal):
    return get_confidence_score(signal) >= CONFIDENCE_THRESHOLD