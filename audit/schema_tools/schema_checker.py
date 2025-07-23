from .log_schemas import LOG_SCHEMA_V1

def check_missing_keys(log):
    return [key for key in LOG_SCHEMA_V1 if key not in log]

def check_type_mismatches(log):
    return {key: type(log[key]) for key in LOG_SCHEMA_V1 if key in log and not isinstance(log[key], LOG_SCHEMA_V1[key])}

