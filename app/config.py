import json

from pathlib import Path
from app.utils import clear_screen


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"
LOGS_PATH = PROJECT_ROOT / "logs"


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
    
def ensure_logs_folder() -> Path:
    """
    Create the logs folder if it does not exist.
    """

    LOGS_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    return LOGS_PATH
        
def show_settings_menu() -> None:
    """
    Display and manage VidPack configuration settings.
    """

    while True:
        clear_screen()

        config = load_config()

        last_preset = config.get(
            "last_preset",
            "Not set",
        )

        last_output_folder = config.get(
            "last_output_folder",
            "Not set",
        )

        print()
        print("Settings")
        print("========")
        print(f"Last preset        : {last_preset}")
        print(f"Last output folder : {last_output_folder}")
        print()
        print("[1] Clear remembered preset")
        print("[2] Clear remembered output folder")
        print("[3] Reset all settings")
        print("[0] Back")
        print()

        choice = input("> ").strip()

        if choice == "1":
            config.pop("last_preset", None)

            if save_config(config):
                print("\n✅ Remembered preset cleared.\n")
            else:
                print("\n❌ Unable to save settings.\n")

        elif choice == "2":
            config.pop("last_output_folder", None)

            if save_config(config):
                print("\n✅ Remembered output folder cleared.\n")
            else:
                print("\n❌ Unable to save settings.\n")

        elif choice == "3":
            confirm = input(
                "Reset all settings? (Y/N): "
            ).strip().lower()

            if confirm in ("y", "yes"):
                if save_config({}):
                    print("\n✅ All settings reset.\n")
                else:
                    print("\n❌ Unable to reset settings.\n")

            else:
                print("\nReset cancelled.\n")

        elif choice == "0":
            return

        else:
            print("\n❌ Invalid choice.\n")