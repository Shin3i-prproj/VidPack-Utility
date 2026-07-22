import os


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """

    command = "cls" if os.name == "nt" else "clear"
    os.system(command)