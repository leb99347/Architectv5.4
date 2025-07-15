# core/shadow_logger.py

import os
import json
from datetime import datetime
from core.log_schemas import format_trade_log

SHADOW_LOG_PATH = "logs/shadow_log.jsonl"

def log_shadow_trade(trade_data):
    os.makedirs(os.path.dirname(SHADOW_LOG_PATH), exist_ok=True)
    trade_data["timestamp"] = datetime.utcnow().isoformat()
    entry = format_trade_log(trade_data)
    with open(SHADOW_LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")