# ml/generate_training_data.py

import os
import json
import pandas as pd
from ml.feature_utils import validate_signal

LOG_PATH = "logs/trade_log.jsonl"
OUTPUT_FEATURES = "ml/training_data.csv"
OUTPUT_LABELS = "ml/training_labels.csv"
TARGET_VERSION = "impact_breakout_v5.4"

def extract_training_data():
    features = []
    labels = []

    if not os.path.exists(LOG_PATH):
        print(f"❌ Log file not found: {LOG_PATH}")
        return [], []

    with open(LOG_PATH, "r") as f:
        for line in f:
            trade = json.loads(line)

            # 🔒 Skip if version mismatch or data is incomplete
            if trade.get("strategy_version") != TARGET_VERSION:
                continue
            if "result" not in trade or "entry_features" not in trade:
                continue

            # 🧠 Binary label
            label = 1 if trade["result"] == "win" else 0

            # ✅ Validate and standardize input features
            signal = validate_signal(trade["entry_features"])

            features.append(signal)
            labels.append(label)

    return features, labels

def save_to_csv(features, labels):
    df = pd.DataFrame(features)
    df["label"] = labels
    df.to_csv(OUTPUT_FEATURES, index=False)
    df["label"].to_csv(OUTPUT_LABELS, index=False, header=False)
    print(f"✅ Saved features to {OUTPUT_FEATURES}")
    print(f"✅ Saved labels to {OUTPUT_LABELS}")

if __name__ == "__main__":
    features, labels = extract_training_data()
    if features and labels:
        save_to_csv(features, labels)
    else:
        print("⚠️ No valid trades found for training.")