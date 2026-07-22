from datetime import datetime
from pathlib import Path

from app.config import ensure_logs_folder


def save_compression_log(
    input_path: Path,
    output_path: Path,
    preset_name: str,
    original_size: int,
    compressed_size: int,
    status: str = "SUCCESS",
) -> Path | None:
    """
    Save the details of a completed compression.
    """

    logs_folder = ensure_logs_folder()

    timestamp = datetime.now()

    log_filename = timestamp.strftime(
        "%Y-%m-%d_%H-%M-%S.log"
    )

    log_path = logs_folder / log_filename

    space_saved = original_size - compressed_size

    log_content = f"""VidPack Compression Log
=======================

Date:
{timestamp.strftime("%Y-%m-%d %H:%M:%S")}

Input:
{input_path}

Output:
{output_path}

Preset:
{preset_name}

Original Size:
{format_file_size(original_size)}

Compressed Size:
{format_file_size(compressed_size)}

Space Saved:
{format_file_size(space_saved)}

Status:
{status}
"""

    try:
        log_path.write_text(
            log_content,
            encoding="utf-8",
        )

        return log_path

    except OSError:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Convert a file size in bytes into a readable value.
    """

    size = float(size_bytes)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"

def get_available_logs() -> list[Path]:
    """
    Return all available log files, newest first.
    """

    logs_folder = ensure_logs_folder()

    logs = list(
        logs_folder.glob("*.log")
    )

    return sorted(
        logs,
        key=lambda log: log.stat().st_mtime,
        reverse=True,
    )

def display_available_logs(
    logs: list[Path],
) -> None:
    """
    Display the available compression logs.
    """

    print()
    print("Compression Logs")
    print("================")

    if not logs:
        print("\nNo compression logs found.\n")
        return

    for index, log_path in enumerate(
        logs,
        start=1,
    ):
        print(f"[{index}] {log_path.name}")

    print()
    print("[0] Back")
    print()

def display_log_contents(
    log_path: Path,
) -> None:
    """
    Display the contents of a compression log.
    """

    print()
    print("=" * 60)

    try:
        print(
            log_path.read_text(
                encoding="utf-8",
            )
        )

    except OSError:
        print("❌ Unable to read the log file.")

    print("=" * 60)

def view_logs() -> None:
    """
    Display and open compression logs.
    """

    while True:
        logs = get_available_logs()

        display_available_logs(logs)

        if not logs:
            try:
                input("Press Enter to return...")
            except EOFError:
                pass

            return

        try:
            choice = input("> ").strip()
        except EOFError:
            print("\nReturning to the previous menu...")
            return

        if choice == "0":
            return

        if not choice.isdigit():
            print("\n❌ Invalid choice.\n")
            continue

        index = int(choice) - 1

        if not (0 <= index < len(logs)):
            print("\n❌ Invalid choice.\n")
            continue

        display_log_contents(logs[index])

        try:
            input("\nPress Enter to continue...")
        except EOFError:
            return