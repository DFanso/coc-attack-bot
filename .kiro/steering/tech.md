# Technology Stack

## Core Technologies
- **Python 3.8+**: Main programming language
- **Windows-specific**: Uses pywin32 for Windows API integration
- **No build system**: Direct Python execution, no compilation required

## Key Dependencies
- **pyautogui**: GUI automation (mouse/keyboard control)
- **keyboard**: Global hotkey detection and handling
- **pywin32**: Windows API access for window detection
- **opencv-python**: Image processing and template matching
- **Pillow**: Image manipulation and screenshot handling
- **numpy**: Numerical operations for image processing
- **requests**: HTTP utilities (future features)

## Common Commands

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot (interactive mode)
python main.py

# Run via batch script (Windows)
run_bot.bat

# Programmatic usage example
python example_usage.py
```

### Development
```bash
# Check Python version (3.8+ required)
python --version

# Verify dependencies
pip show pyautogui keyboard pywin32

# View logs
type logs\coc_bot_YYYYMMDD.log
```

## Configuration
- **config.json**: Main configuration file with hotkeys, directories, and automation settings
- **JSON-based**: All data storage uses JSON format (coordinates, recordings, config)
- **File-based persistence**: No database, uses local file system for all data

## Architecture Patterns
- **MVC-like structure**: Controller (BotController), UI (ConsoleUI), Core modules
- **Modular design**: Separate modules for each major feature (recording, playback, mapping)
- **Dependency injection**: Controller manages all core components
- **Event-driven**: Hotkey-based user interactions
- **Logging-first**: Comprehensive logging throughout all operations