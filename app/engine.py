import subprocess


def run_ffmpeg(command: list[str]) -> subprocess.Popen[str]:
    """
    Start an FFmpeg process and return the running subprocess.
    """

    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )