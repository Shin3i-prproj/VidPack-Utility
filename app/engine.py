import subprocess


def run_ffmpeg(command: list[str]) -> subprocess.Popen[str]:
    """
    Start an FFmpeg process and return the running subprocess.

    FFmpeg output is decoded as UTF-8. Invalid byte sequences are replaced
    instead of terminating the compression process.
    """

    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )