"""
Live confidence model loader and fallback scorer.
Used in production signal routing.
"""

import joblib
import os
import logging
import numpy as np
from ml.confidence_model import rule_based_score as fallback_score

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
        proba = model.predict_proba([features])[0]

        if len(proba) < 2:
            logging.warning("[ML] Model only returns one class probability — returning that as confidence.")
            return round(proba[0], 3)

        return round(proba[1], 3)
    except Exception as e:
        logging.error(f"[ML] Error during live scoring: {e}")
        return fallback_score(signal_dict)

def extract_features(signal):
    """
    Extracts the 4 features the ML model was trained on.
    """
    return [
        int(signal.get("trend_alignment", False)),
        float(signal.get("breakout_strength", 0.0)),
        float(signal.get("multi_tap_score", 0.0)),
        min(1.0, float(signal.get("atr_ratio", 1.0)) / 2.0)
    ]
def extract_extended_features(signal):
    return [
        int(signal.get("trend_alignment", False)),           # 1
        float(signal.get("breakout_strength", 0.0)),         # 2
        float(signal.get("multi_tap_score", 0.0)),           # 3
        min(1.0, float(signal.get("atr_ratio", 1.0)) / 2.0),  # 4
        int(signal.get("doji", False)),                      # 5
        int(signal.get("pivot_zone", False)),                # 6
        int(signal.get("ema_filter", False)),                # 7
        float(signal.get("volatility_score", 0.0)),          # 8
        int(signal.get("session_filter", False)),            # 9 ✅
        int(signal.get("atr_filter", False))                 # 10 ✅
    ]


# ✅ Optional test block
if __name__ == "__main__":
    test_signal = {
        "trend_alignment": True,
        "breakout_strength": 0.82,
        "multi_tap_score": 0.75,
        "atr_ratio": 1.4
    }
    print("Live score:", live_score(test_signal))