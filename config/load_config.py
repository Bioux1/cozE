import json

def init():
    with open("config/config.json", "r") as f:
        return json.load(f)
