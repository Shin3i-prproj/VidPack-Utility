import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"


def load_config() -> dict:
    """
    Load the application configuration from config.json.
    """

    if not CONFIG_PATH.exists():
        return {}

    try:
        with CONFIG_PATH.open(
            "r",
            encoding="utf-8",
        ) as config_file:
            return json.load(config_file)

    except (OSError, json.JSONDecodeError):
        return {}


def save_config(config: dict) -> bool:
    """
    Save the application configuration to config.json.
    """

    print(f"\nSaving config to:\n{CONFIG_PATH}\n")

    try:
        with CONFIG_PATH.open(
            "w",
            encoding="utf-8",
        ) as config_file:
            json.dump(
                config,
                config_file,
                indent=4,
            )

        return True

    except OSError:
        return False
        
    