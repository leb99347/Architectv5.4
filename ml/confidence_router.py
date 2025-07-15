# ml/confidence_router.py

import joblib
from ml.feature_utils import validate_signal

# 🔁 Model ID → .pkl file path
MODEL_PATHS = {
    "4f": "ml/trained_confidence_model_basic.pkl"
}

# 🔁 Load models into memory at startup
MODELS = {
    model_id: joblib.load(path)
    for model_id, path in MODEL_PATHS.items()
}

def score_signal(signal_dict, model_id="4f"):
    """
    Score a signal using the specified model ID.
    Returns a confidence value between 0.0 and 1.0
    """
    if model_id not in MODELS:
        raise ValueError(f"Unknown model ID: {model_id}")
    
    model = MODELS[model_id]
    features = validate_signal(signal_dict, model_id=model_id)
    score = model.predict_proba([features])[0][1]  # class 1 = trade-worthy
    return score