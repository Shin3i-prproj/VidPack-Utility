class VidPackError(Exception):
    """Base exception for all VidPack errors."""


class FFprobeError(VidPackError):
    """Raised when FFprobe fails to read a video."""


class FFmpegError(VidPackError):
    """Raised when FFmpeg fails during compression."""


class InvalidVideoError(VidPackError):
    """Raised when a video cannot be processed."""