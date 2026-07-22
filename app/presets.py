Preset = dict[str, str | int]

COMPRESSION_PRESETS: dict[str, dict[str, str | int]] = {
    "light": {
        "name": "Light Compression",
        "crf": 23,
        "speed": "fast",
    },
    "balanced": {
        "name": "Balanced Compression",
        "crf": 28,
        "speed": "medium",
    },
    "maximum": {
        "name": "Maximum Compression",
        "crf": 32,
        "speed": "slow",
    },
}