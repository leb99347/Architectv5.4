"""
Live confidence model loader and fallback scorer.
Used in production signal routing.
"""

import joblib
import os
import logging
import numpy as np
from ml.confidence_model import score_signal as fallback_score

MODEL_PATH = "ml/trained_confidence_model.pkl"

def live_score(signal_dict):
    """
    Attempts to load a trained model and score the signal.
    Falls back to rule-based score if model is missing or errors occur.
    """
    if not os.path.exists(MODEL_PATH):
        logging.warning("[ML] No trained model found — using fallback rule-based scoring.")
        return fallback_score(signal_dict)

    try:
        model = joblib.load(MODEL_PATH)
        features = extract_features(signal_dict)
        score = model.predict_proba([features])[0][1]
        return round(score, 3)
    except Exception as e:
        logging.error(f"[ML] Error during live scoring: {e}")
        return fallback_score(signal_dict)

def extract_features(signal):
    """
    Extracts numeric features from signal dictionary.
    Used as model input format.
    """
    return [
        int(signal.get('trend_alignment', False)),
        float(signal.get('breakout_strength', 0.0)),
        float(signal.get('multi_tap_score', 0.0)),
        min(1.0, float(signal.get('atr_ratio', 1.0)) / 2.0)
    ]