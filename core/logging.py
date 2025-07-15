import json, os
from datetime import datetime

LOG_VERSION = "v5.4"

def log_event(module: str, event_type: str, payload: dict):
    """
    Logs a structured event to a JSONL file.

    Args:
        module (str): The system module name (e.g., "news_filter", "exit_engine").
        event_type (str): The type of event (e.g., "block", "error", "override").
        payload (dict): The data associated with the event.
    """
    payload = dict(payload)  # ensure shallow copy
    payload["timestamp"] = datetime.utcnow().isoformat()
    payload.setdefault("version", LOG_VERSION)

    safe_module = module.replace(" ", "_").lower()
    safe_event = event_type.replace(" ", "_").lower()

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    path = f"{log_dir}/{safe_module}_{safe_event}.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(payload) + "\n")