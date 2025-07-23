from core.log_keys import LOG_KEYS

def apply_tags(trade_data: dict) -> dict:
    trade_data.setdefault(LOG_KEYS["exit_reason"], "unknown")
    trade_data.setdefault(LOG_KEYS["model_used"], "f10")
    trade_data.setdefault(LOG_KEYS["drawdown_flag"], False)
    trade_data.setdefault(LOG_KEYS["news_conflict"], False)
    return trade_data
