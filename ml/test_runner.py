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
MODEL_PATHS = [
    "ml/models/trained_confidence_model_f4.pkl",
    "ml/models/trained_confidence_model_f10.pkl"
]

for path in MODEL_PATHS:
    print(f"\n📂 Checking model file: {path}")
    if os.path.exists(path):
        try:
            model = joblib.load(path)
            print("✅ Model loaded successfully.")
        except Exception:
            print("❌ Failed to load model:")
            traceback.print_exc()
    else:
        print("❌ Model file not found.")



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
# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)