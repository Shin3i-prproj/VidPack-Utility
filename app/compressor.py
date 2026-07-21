import json
import subprocess
from pathlib import Path

from app.presets import COMPRESSION_PRESETS


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

    preset_choices = {
        "1": "light",
        "2": "balanced",
        "3": "maximum",
    }

    while True:
        choice = input("Select a preset: ").strip()

        if choice == "0":
            return None

        preset_key = preset_choices.get(choice)

        if preset_key:
            return COMPRESSION_PRESETS[preset_key]

        print("\nInvalid option. Please enter 1, 2, 3, or 0.\n")

def build_ffmpeg_command(input_path, preset):
    output_path = input_path.with_name(
        f"{input_path.stem}_compressed.mp4"
    )

    command = [
        "ffmpeg",
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-crf",
        str(preset["crf"]),
        "-preset",
        preset["speed"],
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        str(output_path),
    ]

    return command, output_path

def run_compression(command):
    print()
    print("Starting compression...")
    print()

    try:
        subprocess.run(command, check=True)
        return True

    except FileNotFoundError:
        print("FFmpeg was not found.")
        print("Make sure FFmpeg is installed and added to PATH.")
        return False

    except subprocess.CalledProcessError:
        print("Compression failed while FFmpeg was running.")
        return False