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
        return

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print("\n❌ Unsupported video format.")
        return

    print("\n✅ Video accepted!")
    print(f"File: {path.name}")