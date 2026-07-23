# Changelog

## [1.0.1] - 2026-07-23

### Fixed

- Fixed crashes when processing videos with Unicode or special characters in filenames and metadata
- Improved FFmpeg and FFprobe output decoding on Windows
- Added safer FFprobe JSON validation and error handling

## [1.0.0] - Initial Release

### Added

- Single video compression
- Batch compression
- Compression presets
- Live progress bar
- ETA estimation
- Compression logs
- Configuration system
- About page
- Version management

### Changed

- Refactored the compression workflow into reusable functions
- Improved launcher structure
- Improved code organization
- Added persistent configuration for presets and output folders

### Fixed

- Fixed remembered preset saving
- Fixed output folder persistence
- Fixed batch compression workflow
