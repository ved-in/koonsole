import json

CONFIG = None

def load_config():
    global CONFIG

    if CONFIG is None:
        with open("config.json", "r") as f:
            CONFIG = json.load(f)

    return CONFIG

def get_data(key):
    config = load_config()
    return config[key]
