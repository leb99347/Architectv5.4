# ml/feature_utils.py

import json
import os

SCHEMA_PATH = "ml/feature_schema.json"

def load_schema(model_id="4f"):
    """
    Loads the correct schema based on model ID.
    - '4f' → feature_schema.json
    - '10f' → feature_schema_full.json
    """
    path = "ml/feature_schema.json" if model_id == "4f" else "ml/feature_schema_full.json"
    with open(path, "r") as f:
        return json.load(f)

def validate_signal(signal, model_id="4f"):
    """
    Validates and transforms a signal dictionary based on the selected model's schema.
    Returns a list of features in schema order.
    """
    schema = load_schema(model_id)
    validated = {}

    for key, meta in schema.items():
        raw = signal.get(key, meta.get("default"))
        value = raw

        # Type conversion
        if meta["type"] == "bool":
            value = bool(raw)
        elif meta["type"] == "int":
            value = int(raw)
        elif meta["type"] == "float":
            try:
                value = float(raw)
            except ValueError:
                value = float(meta.get("default", 0.0))

        # Transform logic (custom for atr_ratio)
        if key == "atr_ratio" and "transform" in meta:
            value = min(1.0, value / 2.0)

        validated[key] = value

    # 🔁 Return feature vector as ordered list
    return [validated[key] for key in schema.keys()]