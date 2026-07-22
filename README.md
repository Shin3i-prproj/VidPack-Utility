# 🎬 VidPack Utility

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

**Fast • Clean • Powerful**

VidPack Utility is a lightweight command-line application that uses FFmpeg to compress videos while maintaining excellent visual quality.

Whether you need to reduce the size of a single video or compress an entire folder, VidPack Utility provides a simple, fast, and reliable workflow with live progress tracking and detailed compression logs.

---

## ✨ Features

- 📹 Single video compression
- 📁 Batch folder compression
- 📂 Automatically saves compressed videos to the output folder
- ⚡ Three compression presets
  - Light
  - Balanced
  - Maximum
- 📊 Live progress bar with ETA
- 📝 Compression logs
- ⚙️ Persistent settings
- 🛡️ Error handling
- 💻 Cross-platform terminal support

---

## 🎞 Supported Formats

VidPack Utility supports any video format that FFmpeg can read, including:

- MP4
- MKV
- AVI
- MOV
- WMV
- FLV
- WebM
- M4V
- and many more...

---

## 💡 Why VidPack Utility?

- Lightweight and easy to use
- No unnecessary dependencies
- Real-time compression progress
- Clean command-line interface
- Batch processing support
- Built with Python and FFmpeg

---

## 📷 Preview

### Main Menu

![Main Menu](assets/main-menu.png)

### Compression Progress

![Progress](assets/progress.png)

---

## 📦 Requirements

- Python 3.11+
- FFmpeg
- FFprobe

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/VidPack-Utility.git
cd VidPack-Utility
```

Copy the example configuration:

```bash
cp config.example.json config.json
```

On Windows, simply duplicate `config.example.json` and rename the copy to `config.json`.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python launcher.py
```

---

## 🗂️ Project Structure

```text
VidPack Utility

launcher.py

app/
├── about.py
├── compressor.py
├── config.py
├── engine.py
├── exceptions.py
├── logs.py
├── menu.py
├── presets.py
├── progress.py
├── utils.py
└── version.py
```

---

## 🎯 Compression Presets

| Preset | CRF | Speed |
|--------|----:|--------|
| Light | 23 | fast |
| Balanced | 28 | medium |
| Maximum | 32 | slow |

---

## ⚠ Known Limitations

- Hardware acceleration is not yet supported.
- Custom compression settings are planned for a future release.
- GUI version is planned for v2.0.

---

## 🚀 Roadmap

### v1.1

- Custom CRF
- Hardware acceleration (NVENC / AMF / Quick Sync)
- Additional output formats
- Better logging

### v1.2

- Custom presets
- Recursive folder scanning
- Audio bitrate options

### v2.0

- Graphical User Interface (GUI)
- Drag-and-drop support
- User-defined presets
- Theme support

---

## 📄 License

MIT License

---

## 👤 Author

Shin

---
