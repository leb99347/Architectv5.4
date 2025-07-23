import json
import os
from datetime import datetime

EVENT_LOG_PATH = "logs/trade_executor_executed.jsonl"

def log_event(source: str, event_type: str, payload: dict):
    try:
        os.makedirs(os.path.dirname(EVENT_LOG_PATH), exist_ok=True)
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "event": event_type,
            "data": payload
        }
        with open(EVENT_LOG_PATH, "a") as f:
            f.write(json.dumps(event) + "\n")
        print(f"[📘] Event logged: {event_type} from {source}")
    except Exception as e:
        print(f"[⚠️] Event logging failed: {e}")
