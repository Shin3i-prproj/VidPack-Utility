import json
import subprocess
from pathlib import Path
from tkinter import Tk, filedialog
from app.engine import run_ffmpeg

from app.presets import COMPRESSION_PRESETS


SUPPORTED_VIDEO_EXTENSIONS = {
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

    if path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
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


def display_video_info(path):
    info = get_video_info(path)

    format_info = info["format"]

    video_stream = next(
        stream
        for stream in info["streams"]
        if stream["codec_type"] == "video"
    )

    filename = path.name
    size = int(format_info["size"])
    duration = float(format_info["duration"])
    width = video_stream["width"]
    height = video_stream["height"]

    minutes = int(duration // 60)
    seconds = int(duration % 60)

    print("─" * 60)
    print("Video Information")
    print("─" * 60)
    print(f"Filename   : {filename}")
    print(f"Size       : {size / (1024 * 1024):.2f} MB")
    print(f"Duration   : {minutes}m {seconds}s")
    print(f"Resolution : {width} x {height}")
    print("─" * 60)

    return info


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

def get_available_output_path(input_path):
    output_path = input_path.with_name(
        f"{input_path.stem}_compressed.mp4"
    )

    counter = 1

    while output_path.exists():
        output_path = input_path.with_name(
            f"{input_path.stem}_compressed_{counter}.mp4"
        )
        counter += 1

    return output_path

def build_ffmpeg_command(input_path, preset):
    output_path = get_available_output_path(input_path)

    command = [
        "ffmpeg",
        "-i",
        str(input_path),

        "-progress",
        "pipe:1",
        "-nostats",

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

def run_compression(command, duration):
    print()
    print("Starting compression...")
    print()

    try:
        process = run_ffmpeg(command)

        if process.stdout is None:
            print("Unable to read FFmpeg output.")
            return False

        progress_data = {
            "frame": "0",
            "fps": "0",
            "out_time_ms": "0",
            "speed": "0x",
        }

        for line in process.stdout:
            line = line.strip()

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            if key in progress_data:
                progress_data[key] = value

            if key == "progress":
                out_time_value = progress_data["out_time_ms"]

                if out_time_value == "N/A":
                    continue

                try:
                    out_time_seconds = int(out_time_value) / 1_000_000
                except ValueError:
                    continue

                percentage = min(
                    (out_time_seconds / duration) * 100,
                    100,
                )

                speed_text = progress_data["speed"]

                try:
                    speed = float(speed_text.rstrip("x"))
                except ValueError:
                    speed = 1.0

                remaining_seconds = max(duration - out_time_seconds, 0)

                if speed > 0:
                    eta_seconds = int(remaining_seconds / speed)
                else:
                    eta_seconds = 0

                eta_minutes = eta_seconds // 60
                eta_secs = eta_seconds % 60

                eta = f"{eta_minutes:02}:{eta_secs:02}"

                bar_length = 30
                filled_length = int(bar_length * percentage / 100)

                progress_bar = (
                    "█" * filled_length
                    + "-" * (bar_length - filled_length)
                )

                if value == "end":
                    percentage = 100.0

                    filled_length = bar_length
                    progress_bar = "█" * bar_length
                    eta = "00:00"

                status_line = (
                    f"[{progress_bar}] "
                    f"{percentage:6.2f}% | "
                    f"ETA: {eta} | "
                    f"Frame: {progress_data['frame']} | "
                    f"Speed: {progress_data['speed']}"
                )

                print(
                    f"\r{status_line:<100}",
                    end="",
                    flush=True,
                )

        process.wait()
        print()

        return process.returncode == 0

    except FileNotFoundError:
        print("FFmpeg was not found.")
        print("Make sure FFmpeg is installed and added to PATH.")
        return False
    
def display_compression_results(input_path, output_path):
    original_size = input_path.stat().st_size
    output_size = output_path.stat().st_size
    saved_size = original_size - output_size

    original_size_mb = original_size / (1024 * 1024)
    output_size_mb = output_size / (1024 * 1024)
    saved_size_mb = saved_size / (1024 * 1024)

    if original_size > 0:
        reduction_percentage = (
            saved_size / original_size
        ) * 100
    else:
        reduction_percentage = 0

    print()
    print("Compression Results")
    print("─" * 60)
    print(f"Original size : {original_size_mb:.2f} MB")
    print(f"Output size   : {output_size_mb:.2f} MB")

    if saved_size >= 0:
        print(f"Space saved   : {saved_size_mb:.2f} MB")
        print(f"Reduction     : {reduction_percentage:.2f}%")
    else:
        print(f"Size increase : {abs(saved_size_mb):.2f} MB")
        print(f"Increase      : {abs(reduction_percentage):.2f}%")

    print("─" * 60)

def find_videos_in_folder(folder_path):
    videos = []

    for item in folder_path.iterdir():
        if (
            item.is_file()
            and item.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS
        ):
            videos.append(item)

    return sorted(
        videos,
        key=lambda video: video.name.lower(),
    )

def display_video_list(videos):
    print()
    print(f"Found {len(videos)} video(s):")
    print("─" * 60)

    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video.name}")

    print("─" * 60)

def get_video_duration(video_info):
    def parse_duration(value):
        if value is None:
            return None

        try:
            duration = float(value)

            if duration > 0:
                return duration
        except (TypeError, ValueError):
            pass

        try:
            hours, minutes, seconds = str(value).split(":")

            duration = (
                int(hours) * 3600
                + int(minutes) * 60
                + float(seconds)
            )

            if duration > 0:
                return duration
        except (TypeError, ValueError):
            pass

        return None

    format_info = video_info.get("format", {})

    duration = parse_duration(
        format_info.get("duration")
    )

    if duration is not None:
        return duration

    format_tags = format_info.get("tags", {})

    for key, value in format_tags.items():
        if key.lower() == "duration":
            duration = parse_duration(value)

            if duration is not None:
                return duration

    for stream in video_info.get("streams", []):
        duration = parse_duration(
            stream.get("duration")
        )

        if duration is not None:
            return duration

        duration_ts = stream.get("duration_ts")
        time_base = stream.get("time_base")

        if duration_ts is not None and time_base:
            try:
                numerator, denominator = time_base.split("/")

                duration = (
                    int(duration_ts)
                    * int(numerator)
                    / int(denominator)
                )

                if duration > 0:
                    return duration
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        stream_tags = stream.get("tags", {})

        for key, value in stream_tags.items():
            if key.lower() == "duration":
                duration = parse_duration(value)

                if duration is not None:
                    return duration

    return None

def compress_video(video, preset):
    video_info = get_video_info(video)
    duration = get_video_duration(video_info)

    if duration is None or duration <= 0:
        print(f"❌ Unable to determine duration: {video.name}")
        return False

    command, output_path = build_ffmpeg_command(
        video,
        preset,
    )

    success = run_compression(
        command,
        duration,
    )

    if success:
        display_compression_results(
            video,
            output_path,
        )
    else:
        print(f"❌ Compression failed: {video.name}")

    return success

def compress_video_batch(videos, preset):
    print()
    print("Starting batch compression...")
    print()

    succeeded = 0
    failed = 0

    for index, video in enumerate(videos, start=1):
        print(f"[{index}/{len(videos)}] {video.name}")

        if compress_video(video, preset):
            succeeded += 1
        else:
            failed += 1

        print()

    print("─" * 60)
    print("Batch Complete")
    print("─" * 60)
    print(f"Videos found : {len(videos)}")
    print(f"Succeeded    : {succeeded}")
    print(f"Failed       : {failed}")
    print("─" * 60)

def select_folder():
    root = Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="Select a folder containing videos"
    )

    root.destroy()

    if not folder:
        return None

    return Path(folder)