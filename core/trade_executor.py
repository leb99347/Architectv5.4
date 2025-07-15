# core/trade_executor.py

from core.logger import log_trade
from core.shadow_logger import log_shadow_trade
from core.logging import log_event
from core.version_injector import attach_version  # centralized version injection

def execute_trade(trade_data: dict):
    """
    Executes a trade and logs all execution metadata for auditing and traceability.
    """

    # 🧠 Add version info to trade record
    trade_data = attach_version(trade_data)

    # ✅ Log primary trade
    log_trade(trade_data)

    # 🪞 Log shadow copy for review
    log_shadow_trade(trade_data)

    # 🧾 Record execution event
    log_event("trade_executor", "executed", trade_data)