# core/logger.py

import os
import json
from datetime import datetime
from core.log_schemas import format_trade_log

LOG_PATH = "logs/trade_log.jsonl"

def log_trade(trade_data):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    trade_data["timestamp"] = datetime.utcnow().isoformat()
    entry = format_trade_log(trade_data)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
