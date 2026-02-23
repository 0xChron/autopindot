# Changelog

All notable changes to Autopindot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-23

### Added
- Initial release of Autopindot
- Customizable key selection via visual recorder
- Adjustable interval between key presses
- Global F5 hotkey for start/stop toggle
- 5-second startup delay with countdown timer
- Modern dark-themed UI with Segoe UI font
- Real-time status updates
- Dynamic subtitle showing current configuration
- Number-only validation for interval input
- Window icon support

### Features
- **Key Recorder**: Visual modal window to capture any key press
- **Toggle Button**: Single button that switches between Start/Stop states
- **Status Display**: Shows current state (Idle/Starting/Running/Stopped)
- **Countdown Timer**: Visual feedback during startup delay
- **Input Validation**: Prevents invalid interval values

### Technical
- Built with Python 3.10+
- Uses PyAutoGUI for key pressing
- Uses keyboard library for global hotkeys
- Tkinter/ttk for modern UI
- PyInstaller for executable creation
