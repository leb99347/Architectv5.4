import json
import os
from datetime import datetime
from config import TRADE_LOG_PATH, VERSION, CONFIDENCE_THRESHOLD
from core.tagger import apply_tags
from core.log_keys import LOG_KEYS

def log_trade(trade_data: dict):
    try:
        os.makedirs(os.path.dirname(TRADE_LOG_PATH), exist_ok=True)
        trade_data["timestamp"] = datetime.utcnow().isoformat()
        trade_data["version"] = VERSION
        tagged_data = apply_tags(trade_data)
        with open(TRADE_LOG_PATH, "a") as f:
            f.write(json.dumps(tagged_data) + "\n")
        print(f"[✅] Trade logged: {tagged_data.get('instrument')} @ {tagged_data.get('entry_price')}")
    except Exception as e:
        print(f"[⚠️] Trade logging failed: {e}")
