# ml/train_confidence_model.py

import os
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

LOG_PATH = "logs/trade_log.jsonl"
MODEL_PATH = "ml/trained_confidence_model.pkl"
TARGET_VERSION = "impact_breakout_v5.4"

def load_trades():
    if not os.path.exists(LOG_PATH):
        print("❌ No trade logs found.")
        return []
    with open(LOG_PATH, "r") as f:
        return [json.loads(line) for line in f]

def extract_features_and_labels(trades):
    X, y = [], []
    for trade in trades:
        entry_features = trade.get("entry_features", {})
        features = [
            int(entry_features.get("trend_alignment", False)),
            float(entry_features.get("breakout_strength", 0.0)),
            float(entry_features.get("multi_tap_score", 0.0)),
            min(1.0, float(entry_features.get("atr_ratio", 1.0)) / 2.0)
        ]
        result = trade.get("result", "unknown")
        if result not in ("win", "loss"):
            continue
        label = 1 if result == "win" else 0
        X.append(features)
        y.append(label)
    return np.array(X), np.array(y)

def train_and_save_model(X, y):
    if len(X) == 0:
        print("⚠️ No valid data to train.")
        return
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("📊 Classification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    print(f"[✔] Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    trades = load_trades()
    X, y = extract_features_and_labels(trades)
    train_and_save_model(X, y)