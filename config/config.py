# config/config.py

import os
from dotenv import load_dotenv
load_dotenv()

# Bot versioning
VERSION = "v5.4"

# Logging paths
LOG_DIR = os.getenv("LOG_DIR", "logs")
TRADE_LOG_PATH = os.path.join(LOG_DIR, f"trades_log_{VERSION}.jsonl")
SHADOW_LOG_PATH = os.path.join(LOG_DIR, f"shadow_trades_log_{VERSION}.jsonl")

# ML model paths
MODEL_PATHS = {
    "f4": "ml/models/trained_confidence_model_f4.pkl",
    "f10": "ml/models/trained_confidence_model_f10.pkl",
    "basic": "ml/trained_confidence_model_basic.pkl"
}

# Confidence threshold
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))

# API keys (optional)
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

# Mode switch (live/backtest/shadow)
MODE = os.getenv("MODE", "live")

# Data path
DATA_PATH = os.getenv("DATA_PATH", "data")