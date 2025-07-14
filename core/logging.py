import json, os
from datetime import datetime

def log_event(module: str, event_type: str, payload: dict):
    payload["timestamp"] = datetime.utcnow().isoformat()
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    path = f"{log_dir}/{module}_{event_type}.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(payload) + "\n")
