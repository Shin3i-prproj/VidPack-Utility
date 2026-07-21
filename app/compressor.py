import json
import subprocess
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".webm",
    ".m4v",
}


def get_video_path():
    print()
    print("Enter the video path")
    print("(You can also drag and drop a file here.)")
    print()

    video = input("> ").strip().strip('"')
    path = Path(video)

    if not path.exists():
        print("\n❌ File not found.")
        return None

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print("\n❌ Unsupported video format.")
        return None

    return path


def get_video_info(path: Path):
    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return json.loads(result.stdout)


def display_video_info(path: Path):
    info = get_video_info(path)

    format_info = info.get("format", {})
    streams = info.get("streams", [])

    video_stream = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == "video"
        ),
        {},
    )

    filename = path.name

    size_bytes = int(format_info.get("size", 0))
    size_mb = size_bytes / (1024 * 1024)

    duration = float(format_info.get("duration", 0))
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    width = video_stream.get("width", "?")
    height = video_stream.get("height", "?")

    print()
    print("─" * 60)
    print("Video Information")
    print("─" * 60)
    print(f"Filename   : {filename}")
    print(f"Size       : {size_mb:.2f} MB")
    print(f"Duration   : {minutes}m {seconds}s")
    print(f"Resolution : {width} x {height}")
    print("─" * 60)


def confirm_video():
    print()
    print("[1] Continue")
    print("[0] Cancel")
    print()

    while True:
        choice = input("Select an option: ").strip()

        if choice == "1":
            return True

        if choice == "0":
            return False

        print("\nInvalid option. Please enter 1 or 0.\n")

def select_compression_preset():
    print()
    print("Choose Compression Preset")
    print()
    print("[1] Light Compression")
    print("[2] Balanced Compression")
    print("[3] Maximum Compression")
    print()
    print("[0] Cancel")
    print()

    while True:
        choice = input("Select a preset: ").strip()

        if choice == "1":
            return "light"

        if choice == "2":
            return "balanced"

        if choice == "3":
            return "maximum"

        if choice == "0":
            return None

        print("\nInvalid option. Please enter 1, 2, 3, or 0.\n")