# ml/model_summary.py

import joblib

FEATURE_NAMES = [
    "trend_alignment",
    "breakout_strength",
    "multi_tap_score",
    "atr_ratio"
]

MODEL_PATH = "ml/trained_confidence_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("\n🎯 Feature Importances:")
    for name, score in zip(FEATURE_NAMES, model.feature_importances_):
        print(f"  {name:<20}: {round(score, 4)}")
except Exception as e:
    print(f"❌ Failed to load model or display feature importances: {e}")