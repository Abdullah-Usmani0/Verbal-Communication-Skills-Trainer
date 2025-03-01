import json

CONFIG_PATH = "config.json"

def load_config():
    """Loads the configuration file."""
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)
