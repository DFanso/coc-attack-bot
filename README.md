# COC Attack Bot

A Windows automation bot for Clash of Clans that can record attack sessions and replay them automatically.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The author is not responsible for any account bans or other consequences that may result from using this software.

## Features

- 🎯 **Coordinate Mapping** - Record button positions for your screen resolution
- 📹 **Attack Recording** - Record your attack sessions including clicks and timing
- ▶️ **Attack Playback** - Replay recorded attacks automatically
- 🖼️ **Screenshot Capture** - Take screenshots of the game window
- 🎮 **Game Detection** - Automatically detect COC game window
- ⌨️ **Hotkey Controls** - Easy hotkey controls for all functions
- 📊 **Session Management** - Save, load, and manage multiple attack sessions

## Requirements

- Windows 10 or later
- Python 3.8 or later
- Clash of Clans running in full screen or windowed mode
- Compatible with emulators (BlueStacks, NoxPlayer, etc.)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd coc-attack-bot
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

## Quick Start Guide

### 1. Initial Setup

1. Open Clash of Clans in full screen
2. Run the bot: `python main.py`
3. Go to "Game Detection" to verify the bot can find your game window
4. Take a screenshot to confirm the capture area

### 2. Map Button Coordinates

1. Select "Coordinate Mapping" from the main menu
2. Choose "Start coordinate mapping"
3. Move your mouse to important buttons (attack button, troop selection, etc.)
4. Press **F2** to record each position
5. Enter a descriptive name for each button
6. Press **F3** to save all coordinates

### 3. Record an Attack

1. Select "Attack Recording" from the main menu
2. Choose "Start new recording"
3. Enter a name for your attack session
4. **Manual Mode (Recommended):** Press **F6** to record each click precisely
5. Use **F7** to add delays between actions
6. Press **F5** when finished to stop and save the recording

**Note:** Auto-detection is disabled by default to prevent unwanted recordings. You can enable it in the Attack Recording menu if preferred.

### 4. Play Back an Attack

1. Select "Attack Playback" from the main menu
2. Choose "Play attack"
3. Select your recorded session
4. Make sure COC is in the correct state (attack screen, etc.)
5. Press Enter to begin playback

## Controls

### Coordinate Mapping
- **F1** - Start/Stop mapping mode
- **F2** - Record current mouse position
- **F3** - Save coordinates
- **ESC** - Cancel mapping

### Attack Recording
- **F5** - Start/Stop recording
- **F6** - Manual click recording (recommended mode)
- **F7** - Add delay marker
- **ESC** - Cancel recording

**Recording Modes:**
- **Manual Mode (Default):** Use F6 to record each click precisely
- **Auto Mode (Optional):** Enable in menu for automatic click detection

### Attack Playback
- **F8** - Pause/Resume playback
- **F9** - Stop playback
- **ESC** - Emergency stop

## Directory Structure

```
coc-attack-bot/
├── main.py                 # Main entry point
├── src/
│   ├── bot_controller.py   # Main bot logic
│   ├── core/
│   │   ├── screen_capture.py      # Screenshot and window detection
│   │   ├── coordinate_mapper.py   # Button coordinate mapping
│   │   ├── attack_recorder.py     # Attack session recording
│   │   └── attack_player.py       # Attack playback
│   ├── ui/
│   │   └── console_ui.py   # Console user interface
│   └── utils/
│       ├── logger.py       # Logging utility
│       └── config.py       # Configuration management
├── coordinates/            # Saved button coordinates
├── recordings/            # Recorded attack sessions
├── screenshots/           # Captured screenshots
├── templates/             # Image templates (future use)
├── logs/                  # Log files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

The bot creates a `config.json` file with default settings. You can modify this file to customize:

- Hotkey bindings
- Default directories
- Automation settings
- Game detection parameters

## Tips for Best Results

1. **Screen Resolution** - Keep your screen resolution consistent between recording and playback
2. **Game State** - Make sure COC is in the same state when playing back attacks
3. **Practice Mode** - Test your recordings on practice attacks first
4. **Playback Speed** - Use slower speeds (0.5x) for more reliable playback
5. **Supervision** - Always supervise the bot during operation

## Safety Features

- **Failsafe** - Move mouse to top-left corner to stop all automation
- **Emergency Stop** - Press ESC during any operation to stop immediately
- **Validation** - Recordings are validated before playback
- **Logging** - All actions are logged for debugging

## Troubleshooting

### Game Not Detected
- Make sure COC is running and visible
- Try different window modes (full screen vs windowed)
- Check if you're using a supported emulator

### Playback Issues
- Verify coordinates are mapped correctly for your resolution
- Check that the game is in the correct state before playback
- Try slower playback speeds
- Validate recordings before playing them

### Recording Problems
- Make sure the recording hotkeys aren't conflicting with other software
- Check that the bot has proper permissions to detect input
- Verify the screenshots directory is writable

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is provided as-is for educational purposes. Use responsibly and at your own risk.

## Support

If you encounter issues:

1. Check the log files in the `logs/` directory
2. Verify your Python and package versions
3. Make sure COC is running and detectable
4. Try the built-in validation tools

---

**Remember: This bot is for educational purposes only. Always follow the game's terms of service and use responsibly.** 