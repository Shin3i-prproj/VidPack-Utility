import json
import subprocess

from json import JSONDecodeError

from tkinter import Tk, filedialog

from app.engine import run_ffmpeg
from app.exceptions import FFmpegError, FFprobeError
from app.presets import COMPRESSION_PRESETS
from app.progress import monitor_progress
from app.config import load_config, save_config


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


def get_video_info(path: Path) -> dict:
    """
    Retrieve video metadata using FFprobe.
    """
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

    if result.returncode != 0:
        raise FFprobeError(result.stderr.strip())

    try:
        return json.loads(result.stdout)
    except JSONDecodeError as error:
        raise FFprobeError(
            "FFprobe returned invalid data."
        ) from error


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

def select_compression_preset() -> dict | None:
    """
    Ask the user to select a compression preset.

    Pressing Enter reuses the last valid preset.
    """

    config = load_config()
    last_preset_name = config.get("last_preset")

    preset_choices = {
        "1": "light",
        "2": "balanced",
        "3": "maximum",
    }

    preset_names = {
        preset["name"]: preset
        for preset in COMPRESSION_PRESETS.values()
    }

    last_preset = preset_names.get(last_preset_name)

    print()
    print("Choose Compression Preset")
    print()

    if last_preset:
        print(f"⭐ Last used: {last_preset_name}")
        print()

    print("[1] Light Compression")
    print("[2] Balanced Compression")
    print("[3] Maximum Compression")
    print()

    if last_preset:
        print("Press Enter to use the last preset.")

    print("[0] Cancel")
    print()

    while True:
        choice = input("Select a preset: ").strip()

        if choice == "":
            if last_preset:
                print(f"\n⭐ Using last preset: {last_preset_name}\n")
                return last_preset

            print("\nNo previous preset is available.\n")
            continue

        if choice == "0":
            return None

        preset_key = preset_choices.get(choice)

        if preset_key:
            return COMPRESSION_PRESETS[preset_key]

        print("\nInvalid option. Please enter 1, 2, 3, or 0.\n")

def select_output_folder() -> Path:
    """
    Ask the user to choose an output folder.

    Pressing Enter reuses the last valid output folder.
    """

    config = load_config()
    last_output_folder = config.get("last_output_folder")

    saved_output_folder = None

    if last_output_folder:
        candidate_folder = Path(last_output_folder)

        if candidate_folder.exists() and candidate_folder.is_dir():
            saved_output_folder = candidate_folder

    print()
    print("Output Folder")
    print()

    if saved_output_folder:
        print("⭐ Last used:")
        print(saved_output_folder)
        print()
        print("Press Enter to use the last folder.")
        print()

    while True:
        folder_input = input("Enter output folder: ").strip()

        if folder_input == "":
            if saved_output_folder:
                print(
                    f"\n⭐ Using last output folder: "
                    f"{saved_output_folder}\n"
                )
                return saved_output_folder

            print("\nPlease enter an output folder.\n")
            continue

        output_folder = Path(folder_input).expanduser()

        if not output_folder.exists():
            print("\nThat folder does not exist.\n")
            continue

        if not output_folder.is_dir():
            print("\nThe selected path is not a folder.\n")
            continue

        config["last_output_folder"] = str(output_folder)
        save_config(config)

        return output_folder

def get_available_output_path(
    input_path: Path,
    output_folder: Path,
) -> Path:
    output_path = output_folder / (
        f"{input_path.stem}_compressed.mp4"
    )

    counter = 1

    while output_path.exists():
        output_path = output_folder / (
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

def run_compression(
    command: list[str],
    duration: float,
) -> bool:
    print()
    print("Starting compression...")
    print()

    try:
        process = run_ffmpeg(command)

        return monitor_progress(
            process,
            duration,
        )

    except FileNotFoundError as error:
        raise FFmpegError(
            "FFmpeg was not found. Make sure FFmpeg is installed and added to PATH."
        ) from error
    
def display_compression_results(
    input_path: Path,
    output_path: Path,
    preset: dict,
) -> None:
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
    print(f"Preset        : {preset['name']}")
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

def get_video_duration(video_info: dict) -> float | None:
    """
    Extract the video duration in seconds from FFprobe metadata.
    """

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

def compress_video(video: Path, preset: dict) -> bool:
    try:
        video_info = get_video_info(video)
    except FFprobeError as error:
        print(f"\n❌ {error}")
        return False

    duration = get_video_duration(video_info)
    if duration is None:
        print("\n❌ Unable to determine the video's duration.")
        return False

    if duration <= 0:
        print(f"❌ Invalid duration ({duration}) for: {video.name}")
        return False

    command, output_path = build_ffmpeg_command(
        video,
        preset,
    )

    config = load_config()
    config["last_preset"] = preset["name"]

    saved = save_config(config)
    reloaded_config = load_config()

    print()
    print("========== PRESET CONFIG DEBUG ==========")
    print(f"Compressor file : {Path(__file__).resolve()}")
    print(f"Preset received : {preset}")
    print(f"Save successful : {saved}")
    print(f"Reloaded config : {reloaded_config}")
    print("=========================================")
    print()

    try:
        success = run_compression(
            command,
            duration,
        )

    except FFmpegError as error:
        print(f"\n❌ {error}")
        return False

    if success:
        display_compression_results(
            video,
            output_path,
            preset,
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