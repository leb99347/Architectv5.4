# ml/generate_training_data.py

import json
import os
import pandas as pd
from ml.feature_utils import validate_signal

LOG_PATH = "logs/trade_log.jsonl"
OUTPUT_FEATURES = "ml/training_data.csv"
OUTPUT_LABELS = "ml/training_labels.csv"

def extract_training_data():
    features = []
    labels = []

    if not os.path.exists(LOG_PATH):
        print(f"❌ Log file not found: {LOG_PATH}")
        return

    with open(LOG_PATH, "r") as f:
        for line in f:
            trade = json.loads(line)

            if "result" not in trade or "tags" not in trade:
                continue

            # Score is binary: win = 1, loss = 0
            label = 1 if trade["result"] == "win" else 0
            signal = validate_signal(trade["tags"])

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