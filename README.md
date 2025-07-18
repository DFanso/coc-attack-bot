# COC Attack Bot

A Windows automation bot for Clash of Clans that can record attack sessions and replay them automatically with AI-powered base analysis.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The author is not responsible for any account bans or other consequences that may result from using this software.

## Features

- 🎯 **Coordinate Mapping** - Record button positions for your screen resolution
- 📹 **Attack Recording** - Record your attack sessions including clicks and timing
- ▶️ **Attack Playback** - Replay recorded attacks automatically
- 🤖 **AI Base Analysis** - Analyze base loot using Google Gemini AI
- 🏃 **Auto Attacker** - Automatically find and attack bases based on loot requirements
- 🖼️ **Screenshot Capture** - Take screenshots of the game window
- 🎮 **Game Detection** - Automatically detect COC game window
- ⌨️ **Hotkey Controls** - Easy hotkey controls for all functions
- 📊 **Session Management** - Save, load, and manage multiple attack sessions

## Requirements

- Windows 10 or later
- Python 3.8 or later
- **Clash of Clans running in FULL SCREEN mode** (required for all operations)
- Compatible with emulators (BlueStacks, NoxPlayer, etc.)
- Google Gemini API key (for AI analysis features)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/DFanso/coc-attack-bot>
   cd coc-attack-bot
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   ```bash
   # Copy the example configuration file
   copy src\utils\example.config.py src\utils\config.py
   ```

4. **Get a Google Gemini API key:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the API key for the next step

5. **Edit the configuration:**
   - Open `src\utils\config.py` in a text editor
   - Replace the placeholder API key on line 82 with your actual Gemini API key:
     ```python
     "google_gemini_api_key": "YOUR_ACTUAL_API_KEY_HERE",
     ```
   - Set `"enabled": True` on line 83 to enable AI analysis

6. **Run the bot:**
   ```bash
   python main.py
   ```

## Quick Start Guide

**⚠️ IMPORTANT: Always run Clash of Clans in FULL SCREEN mode during all operations!**

### 1. Initial Setup

1. **Open Clash of Clans in FULL SCREEN mode** (this is crucial for accurate coordinates)
2. Run the bot: `python main.py`
3. Go to "Game Detection" to verify the bot can find your game window
4. Take a screenshot to confirm the capture area is correct

### 2. Map Key Coordinates

**This is the most important step - you need to map button positions for your specific screen resolution.**

1. Select "Coordinate Mapping" from the main menu
2. Choose "Start coordinate mapping"
3. Move your mouse to important game elements and press **F2** to record each position:
   - **Attack button** (to start searching for bases)
   - **Next button** (to skip bases during search)
   - **Army camps** (to check if army is ready)
   - **Troop selection buttons** (barbarians, archers, spells, etc.)
   - **Deploy positions** (where to place troops on the base)
   - **Return home button** (after attack completion)
4. Enter descriptive names for each coordinate (e.g., "attack_button", "barbarian", "archer")
5. Press **F3** to save all coordinates when finished

**Essential coordinates to map:**
- `attack_button` - The attack button to start base search
- `next_button` - Skip to next base during search
- `find_a_match` - find a match button

- `barbarian` - Barbarian troop selection
- `archer` - Archer troop selection
- `spell1` - First spell slot
- `return_home` - Return home after attack

### 3. Record Attack Strategies

1. Select "Attack Recording" from the main menu
2. Choose "Start new recording"
3. Enter a descriptive name for your attack strategy (e.g., "barch_collector_raid")
4. **Manual Mode (Recommended):** Press **F6** to record each click precisely
5. Use **F7** to add delays between actions when needed
6. Record a complete attack sequence from troop deployment to completion
7. Press **F5** when finished to stop and save the recording

**Recording Tips:**
- Record different strategies for different base types
- Include delays between troop deployments for better timing
- Record the full sequence including returning home

### 4. Set Up Auto Attacker (AI-Powered)

1. Ensure you have configured your Gemini API key in `src\utils\config.py`
2. Select "Auto Attacker" from the main menu
3. Choose "Start auto attack"
4. Set your minimum loot requirements:
   - Minimum gold (default: 300,000)
   - Minimum elixir (default: 300,000)
   - Minimum dark elixir (default: 2,000)
5. Select the attack strategy you want to use
6. The bot will automatically:
   - Search for bases
   - Analyze loot using AI
   - Attack suitable bases
   - Return home and repeat

### 5. Manual Attack Playback

1. Select "Attack Playback" from the main menu
2. Choose "Play attack"
3. Select your recorded session
4. Make sure COC is in the attack screen with a base loaded
5. Press Enter to begin playback

**Playback Tips:**
- Ensure game state matches when the recording was made
- Use slower playback speeds for more reliable execution
- Always supervise the playback process

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

The bot uses `src\utils\config.py` for all configuration settings. After copying from `example.config.py`, you can modify:

### Essential Settings

**AI Analysis Settings:**
- `google_gemini_api_key` - Your Gemini API key (required for AI features)
- `enabled` - Set to `True` to enable AI base analysis
- `min_gold`, `min_elixir`, `min_dark_elixir` - Minimum loot requirements for auto attacks

**Other Settings:**
- Hotkey bindings for all operations
- Default directories for screenshots, recordings, coordinates
- Automation timing and speed settings
- Game detection parameters

## Tips for Best Results

1. **Full Screen Mode** - **ALWAYS** run Clash of Clans in full screen mode for accurate coordinate mapping
2. **Screen Resolution** - Keep your screen resolution consistent between recording and playback
3. **Game State** - Make sure COC is in the same state when playing back attacks
4. **Coordinate Mapping** - Take time to accurately map all essential buttons and positions
5. **Practice Mode** - Test your recordings on practice attacks first
6. **Playback Speed** - Use slower speeds (0.5x) for more reliable playback
7. **AI Analysis** - Ensure your Gemini API key is valid and has sufficient quota
8. **Supervision** - Always supervise the bot during operation
9. **Army Ready** - Make sure your army is trained before starting auto attacks
10. **Internet Connection** - Stable internet required for AI analysis features

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