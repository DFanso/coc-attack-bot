# Project Structure

## Root Directory Layout
```
coc-attack-bot/
├── main.py                 # Entry point - initializes bot and UI
├── example_usage.py        # Programmatic API usage examples
├── run_bot.bat            # Windows batch launcher script
├── config.json            # Main configuration file
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Source Code Organization (`src/`)
```
src/
├── __init__.py            # Package marker
├── bot_controller.py      # Main controller - orchestrates all components
├── core/                  # Core automation functionality
│   ├── screen_capture.py      # Screenshot and window detection
│   ├── coordinate_mapper.py   # Button coordinate mapping
│   ├── attack_recorder.py     # Attack session recording
│   ├── attack_player.py       # Attack playback engine
│   └── auto_attacker.py       # Automated continuous attacks
├── ui/
│   └── console_ui.py      # Console-based user interface
└── utils/
    ├── logger.py          # Logging utility
    └── config.py          # Configuration management
```

## Data Directories
- **coordinates/**: JSON files with button coordinate mappings
- **recordings/**: JSON files with recorded attack sessions
- **screenshots/**: PNG screenshots for debugging and validation
- **logs/**: Daily log files (coc_bot_YYYYMMDD.log format)
- **templates/**: Image templates for future template matching features

## File Naming Conventions
- **Python files**: snake_case (e.g., `bot_controller.py`)
- **Classes**: PascalCase (e.g., `BotController`, `ScreenCapture`)
- **Methods/functions**: snake_case (e.g., `start_recording()`)
- **Constants**: UPPER_SNAKE_CASE in config
- **Data files**: descriptive names with timestamps where applicable

## Import Patterns
- **Relative imports**: Use relative imports within src package (`from .core import`)
- **Absolute imports**: External libraries use absolute imports
- **Controller pattern**: BotController imports and manages all core components
- **Dependency injection**: Components receive dependencies via constructor

## Configuration Structure
- **Hierarchical JSON**: Nested configuration sections (bot, automation, display, etc.)
- **Environment-specific**: Separate sections for different aspects (hotkeys, directories)
- **Extensible**: Easy to add new configuration sections without breaking existing code