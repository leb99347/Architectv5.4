from .log_schemas import LOG_SCHEMA_V1

def repair_trade(trade):
    repaired = {}
    for key, expected_type in LOG_SCHEMA_V1.items():
        value = trade.get(key)
        if value is None:
            repaired[key] = default_value(expected_type)
        elif not isinstance(value, expected_type):
            try:
                repaired[key] = expected_type(value)
            except:
                repaired[key] = default_value(expected_type)
        else:
            repaired[key] = value
    return repaired

def default_value(t):
    if t == str:
        return 'unknown'
    elif t == float:
        return 0.0
    elif t == dict:
        return {}
    return None

