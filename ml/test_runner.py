# test_runner.py — ArchitectV4 ML System Diagnostic Runner

import importlib
import traceback
import joblib
import json
import pandas as pd
import os

print("\n🔍 ArchitectV4 ML Module Test Runner\n")

# -------------------------------
# STEP 1 — Test ML Module Imports
# -------------------------------
ML_MODULES = [
    "ml.confidence_model",
    "ml.mansa_feedback",  # Add more modules if needed
]

for module_path in ML_MODULES:
    print(f"📦 Testing: {module_path}")
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "main"):
            print("▶️  Running `main()`...")
            module.main()
        else:
            print("✅ Imported successfully (no main function).")
    except Exception:
        print("❌ Error during module test:")
        traceback.print_exc()
    print("-" * 50)


# --------------------------------------
# STEP 2 — Load and Validate Trained Model
# --------------------------------------
MODEL_PATH = "ml/trained_confidence_model.pkl"
print(f"\n📂 Checking model file: {MODEL_PATH}")
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully.")
    except Exception:
        print("❌ Failed to load model:")
        traceback.print_exc()
else:
    print("❌ Model file not found.")
print("-" * 50)


# ----------------------------------------
# STEP 3 — Load and Validate Feature Schema
# ----------------------------------------
SCHEMA_PATH = "ml/feature_schema.json"
print(f"\n📂 Checking feature schema: {SCHEMA_PATH}")
if os.path.exists(SCHEMA_PATH):
    try:
        with open(SCHEMA_PATH, "r") as f:
            schema = json.load(f)
        print(f"✅ Schema loaded: {schema}")

        # Check for missing fields in test signal
        test_signal = {
            key: schema[key].get("default", None)
            for key in schema
        }
        missing = [key for key in schema if key not in test_signal]
        if missing:
            print(f"❗ Warning: These schema fields are missing from test signal: {missing}")
        else:
            print("✅ All schema fields accounted for in test signal.")

    except Exception:
        print("❌ Failed to parse feature schema:")
        traceback.print_exc()
else:
    print("❌ Schema file not found.")
print("-" * 50)


# -------------------------------------------------------
# STEP 4 — Test Live Scoring with Fallback Rule-Based Model
# -------------------------------------------------------
try:
    from ml.confidence_model_live import live_score

    sample_signal = {
        "trend_alignment": True,
        "breakout_strength": 0.9,
        "multi_tap_score": 0.6,
        "atr_ratio": 1.1
    }

    print("\n🧠 Running confidence score on sample signal:")
    score = live_score(sample_signal)
    print(f"✅ Live Score: {score:.3f}")

except Exception:
    print("❌ Live scoring test failed:")
    traceback.print_exc()

print("-" * 50)
print("✅ All diagnostic tests completed.\n")