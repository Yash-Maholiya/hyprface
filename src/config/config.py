import json
from pathlib import Path

CONFIG_FILE = Path("config/config.json")


def save_config(data):
    CONFIG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(CONFIG_FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )


def load_config():

    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)
