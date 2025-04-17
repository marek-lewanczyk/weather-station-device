# config.py

import ujson

def load_config():
    try:
        with open("config.json", "r") as f:
            return ujson.load(f)
    except:
        return {}

config = load_config()