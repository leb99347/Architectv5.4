# core/version_injector.py

try:
    from config.settings import BOT_VERSION
except ImportError:
    BOT_VERSION = "unknown"

def attach_version(data: dict):
    data.setdefault("strategy_version", BOT_VERSION)
    return data