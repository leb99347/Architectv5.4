# ml/feature_utils.py

import json
import os

SCHEMA_PATH = "ml/feature_schema.json"

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def validate_signal(signal):
    """
    Validates and transforms a signal dictionary based on the schema.
    Ensures correct typing, default fallbacks, and normalization.
    """
    schema = load_schema()
    validated = {}

    for key, meta in schema.items():
        raw = signal.get(key, meta.get("default"))
        value = raw

        # Convert type
        if meta["type"] == "bool":
            value = bool(raw)
        elif meta["type"] == "int":
            value = int(raw)
        elif meta["type"] == "float":
            try:
                value = float(raw)
            except ValueError:
                value = float(meta.get("default", 0.0))

        # Apply transform
        if "transform" in meta and key == "atr_ratio":
            value = min(1.0, value / 2.0)

        validated[key] = value

    return validated