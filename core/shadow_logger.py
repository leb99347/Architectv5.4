import json
import os
from datetime import datetime
from config import TRADE_LOG_PATH, VERSION, CONFIDENCE_THRESHOLD, SHADOW_LOG_PATH
from core.tagger import apply_tags

SHADOW_LOG_PATH = "logs/shadow_trades_log_v4.jsonl"

def log_shadow_trade(trade_data: dict):
    try:
        os.makedirs(os.path.dirname(SHADOW_LOG_PATH), exist_ok=True)
        trade_data["timestamp"] = datetime.utcnow().isoformat()
        trade_data["version"] = VERSION
        tagged_data = apply_tags(trade_data)
        with open(SHADOW_LOG_PATH, "a") as f:
            f.write(json.dumps(tagged_data) + "\n")
        print(f"[🪞] Shadow trade logged.")
    except Exception as e:
        print(f"[⚠️] Shadow trade logging failed: {e}")
