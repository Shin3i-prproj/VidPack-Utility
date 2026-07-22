import subprocess


def monitor_progress(
    process: subprocess.Popen,
    duration: float,
) -> bool:
    """
    Monitor FFmpeg progress and display a live progress bar.
    """

    if duration <= 0:
        print("Unable to monitor progress: invalid video duration.")
        return False

    if process.stdout is None:
        print("Unable to read FFmpeg output.")
        return False

    progress_data = {
        "frame": "0",
        "fps": "0",
        "out_time_ms": "0",
        "speed": "0x",
    }

    bar_length = 30

    for line in process.stdout:
        line = line.strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key in progress_data:
            progress_data[key] = value

        if key != "progress":
            continue

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
            speed = 0.0

        remaining_seconds = max(
            duration - out_time_seconds,
            0,
        )

        if speed > 0:
            eta_seconds = int(remaining_seconds / speed)
            eta_minutes = eta_seconds // 60
            eta_secs = eta_seconds % 60
            eta = f"{eta_minutes:02}:{eta_secs:02}"
        else:
            eta = "--:--"

        filled_length = int(
            bar_length * percentage / 100
        )

        progress_bar = (
            "█" * filled_length
            + "-" * (bar_length - filled_length)
        )

        if value == "end":
            percentage = 100.0
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

    if process.returncode == 0:
        final_bar = "█" * bar_length

        final_status = (
            f"[{final_bar}] "
            f"{100.00:6.2f}% | "
            f"ETA: 00:00 | "
            f"Frame: {progress_data['frame']} | "
            f"Speed: {progress_data['speed']}"
        )

        print(
            f"\r{final_status:<100}",
            end="",
            flush=True,
        )

    print()

    return process.returncode == 0