import os
from dotenv import load_dotenv
load_dotenv()

BOT_VERSION = "impact_breakout_v5.4"
MODE = os.getenv("MODE", "live")
TRADE_LOG_PATH = "analytics/trade_log.csv"
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
