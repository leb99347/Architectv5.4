# core/logger.py

import os
import json
from datetime import datetime
from config.settings import BOT_VERSION
from core.log_schemas import format_trade_log
from core.version_injector import attach_version

LOG_PATH = "logs/trade_log.jsonl"

def log_trade(trade_data):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    trade_data["timestamp"] = datetime.utcnow().isoformat()

    # Inject version and defaults
    trade_data = attach_version(trade_data)
    trade_data.setdefault("exit_reason", "unspecified")
    trade_data.setdefault("was_news_blocked", False)

    # Capture key signal metadata for traceability
    tags = trade_data.get("tags", {})
    trade_data["entry_features"] = {
        "trend_alignment": tags.get("trend_alignment", False),
        "breakout_strength": tags.get("breakout_strength", 0.0),
        "multi_tap_score": tags.get("multi_tap_score", 0.0),
        "atr_ratio": tags.get("atr_ratio", 1.0)
    }

    entry = format_trade_log(trade_data)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")