from config.settings import BOT_VERSION

def attach_version(data: dict):
    data["model_version"] = BOT_VERSION
    return data
