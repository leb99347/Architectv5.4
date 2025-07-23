from .log_schemas import LOG_SCHEMA_V1

def validate_log(log):
    for key, expected_type in LOG_SCHEMA_V1.items():
        if key not in log or not isinstance(log[key], expected_type):
            return False
    return True

