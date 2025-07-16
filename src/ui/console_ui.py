"""
Console UI - Command-line interface for the COC Attack Bot
"""

import sys
import os
import time
from typing import Optional
from ..bot_controller import BotController

class ConsoleUI:
    """Console-based user interface for the COC Attack Bot"""
    
    def __init__(self, bot_controller: BotController):
        self.bot = bot_controller
        self.running = True
    
    def run(self) -> None:
        """Main UI loop"""
        self.show_banner()
        
        while self.running:
            try:
                self.show_menu()
                choice = input("\nEnter your choice: ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\nShutting down...")
                self.running = False
            except EOFError:
                print("\n\nShutting down...")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                input("Press Enter to continue...")
        
        self.bot.shutdown()
    
    def show_banner(self) -> None:
        """Display the application banner"""
        print("=" * 60)
        print("        COC ATTACK BOT - Windows Automation")
        print("=" * 60)
        print("  Automated Clash of Clans attack recording and playback")
        print("=" * 60)
    
    def show_menu(self) -> None:
        """Display the main menu"""
        print("\n" + "=" * 40)
        print("           MAIN MENU")
        print("=" * 40)
        print("1. Coordinate Mapping")
        print("2. Attack Recording")
        print("3. Attack Playback")
        print("4. Auto Attack System")
        print("5. Game Detection")
        print("6. Screenshots")
        print("7. Settings")
        print("8. Help")
        print("9. Exit")
        print("=" * 40)
    
    def handle_choice(self, choice: str) -> None:
        """Handle user menu choice"""
        if choice == '1':
            self.coordinate_mapping_menu()
        elif choice == '2':
            self.attack_recording_menu()
        elif choice == '3':
            self.attack_playback_menu()
        elif choice == '4':
            self.auto_attack_menu()
        elif choice == '5':
            self.game_detection_menu()
        elif choice == '6':
            self.screenshots_menu()
        elif choice == '7':
            self.settings_menu()
        elif choice == '8':
            self.show_help()
        elif choice == '9':
            self.running = False
        else:
            print("Invalid choice. Please try again.")
    
    def auto_attack_menu(self) -> None:
        """Automated attack system menu"""
        while True:
            print("\n" + "=" * 40)
            print("       AUTO ATTACK SYSTEM")
            print("=" * 40)
            
            # Show current status
            if self.bot.is_auto_attacking():
                print("Status: RUNNING")
                stats = self.bot.get_auto_attack_stats()
                print(f"Attacks: {stats['total_attacks']} (Success: {stats['success_rate']:.1f}%)")
                print(f"Runtime: {stats['runtime_hours']:.1f} hours")
                print(f"Army Check: DISABLED")
                print(f"Loot Check: ENABLED")
            else:
                print("Status: STOPPED")
            
            print("=" * 40)
            print("1. Setup Auto Attack")
            print("2. Start Auto Attack")
            print("3. Stop Auto Attack")
            print("4. View Statistics")
            print("5. Configure Required Buttons")
            print("6. Back to main menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.setup_auto_attack()
            elif choice == '2':
                self.start_auto_attack()
            elif choice == '3':
                self.stop_auto_attack()
            elif choice == '4':
                self.show_auto_attack_stats()
            elif choice == '5':
                self.configure_auto_attack_buttons()
            elif choice == '6':
                break
            else:
                print("Invalid choice.")
    
    def setup_auto_attack(self) -> None:
        """Setup auto attack configuration"""
        print("\n=== AUTO ATTACK SETUP ===")
        
        # Show available recorded sessions
        sessions = self.bot.list_recorded_attacks()
        if not sessions:
            print("No recorded attack sessions found!")
            print("Please record some attacks first using the Attack Recording menu.")
            return
        
        print("Available attack sessions:")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")
        
        # Select sessions to use
        selected_sessions = []
        while True:
            try:
                choice = input("\nEnter session number to add (0 to finish): ").strip()
                if choice == '0':
                    break
                
                session_idx = int(choice) - 1
                if 0 <= session_idx < len(sessions):
                    session_name = sessions[session_idx]
                    if session_name not in selected_sessions:
                        selected_sessions.append(session_name)
                        print(f"Added: {session_name}")
                    else:
                        print("Session already selected")
                else:
                    print("Invalid session number")
            except ValueError:
                print("Please enter a valid number")
        
        if not selected_sessions:
            print("No sessions selected")
            return

        # AI Configuration
        use_ai = input("\nEnable AI Analysis for this run? (y/n, default y): ").strip().lower()
        use_ai = use_ai != 'n'
        self.bot.config.set('ai_analyzer.enabled', use_ai)
        
        if use_ai:
            api_key = self.bot.config.get('ai_analyzer.google_gemini_api_key')
            if not api_key:
                api_key = input("Please enter your Google Gemini API Key: ").strip()
                if not api_key:
                    print("❌ API Key cannot be empty. Disabling AI analysis.")
                    self.bot.config.set('ai_analyzer.enabled', False)
                else:
                    self.bot.config.set('ai_analyzer.google_gemini_api_key', api_key)
                    self.bot.ai_analyzer.api_key = api_key
            
            if self.bot.config.get('ai_analyzer.enabled'):
                print("Testing AI Connection...")
                if not self.bot.test_ai_connection():
                    print("❌ AI Connection Failed. Check your API key. Disabling AI for this run.")
                    self.bot.config.set('ai_analyzer.enabled', False)
                else:
                    print("✅ AI Connection Successful.")
        
        # Loot requirements
        print("\nSet minimum loot requirements:")
        try:
            min_gold = int(input(f"Minimum Gold (default {self.bot.config.get('ai_analyzer.min_gold')}): ") or self.bot.config.get('ai_analyzer.min_gold'))
            min_elixir = int(input(f"Minimum Elixir (current: {self.bot.config.get('ai_analyzer.min_elixir')}): ") or self.bot.config.get('ai_analyzer.min_elixir'))
            min_dark_elixir = int(input(f"Minimum Dark Elixir (current: {self.bot.config.get('ai_analyzer.min_dark_elixir')}): ") or self.bot.config.get('ai_analyzer.min_dark_elixir'))
            self.bot.config.set('ai_analyzer.min_gold', min_gold)
            self.bot.config.set('ai_analyzer.min_elixir', min_elixir)
            self.bot.config.set('ai_analyzer.min_dark_elixir', min_dark_elixir)
        except ValueError:
            print("Invalid input. Using default loot values.")

        # Final Configuration Summary
        self.bot.config.set('auto_attacker.attack_sessions', selected_sessions)
        self.bot.auto_attacker.attack_sessions = selected_sessions
        self.bot.config.save_config()
        
        print("\n" + "=" * 40)
        print("✅ Auto Attack Configured:")
        print(f"  Attack Sessions: {', '.join(selected_sessions)}")
        print(f"  AI Analysis: {'ENABLED' if self.bot.config.get('ai_analyzer.enabled') else 'DISABLED'}")
        if self.bot.config.get('ai_analyzer.enabled'):
            print(f"    Min Gold: {self.bot.config.get('ai_analyzer.min_gold'):,}")
            print(f"    Min Elixir: {self.bot.config.get('ai_analyzer.min_elixir'):,}")
            print(f"    Min Dark Elixir: {self.bot.config.get('ai_analyzer.min_dark_elixir'):,}")
        print("=" * 40)
        print("Ready to start from the Auto Attack menu!")

    def start_auto_attack(self) -> None:
        """Start the auto attack system"""
        if self.bot.is_auto_attacking():
            print("Auto attack is already running!")
            return
        
        # Ensure sessions are configured before starting
        attack_sessions = self.bot.config.get('auto_attacker.attack_sessions', [])
        if not attack_sessions:
            print("❌ No attack sessions configured! Please run Setup first.")
            return
        
        print("\n" + "=" * 40)
        print("         🚀 STARTING AUTO ATTACK 🚀")
        print("=" * 40)
        print("Configuration for this run:")
        print(f"  Attack Sessions: {', '.join(attack_sessions)}")
        print(f"  AI Analysis: {'ENABLED' if self.bot.config.get('ai_analyzer.enabled') else 'DISABLED'}")
        print(f"  Min Gold: {self.bot.config.get('ai_analyzer.min_gold'):,}")
        print(f"  Min Elixir: {self.bot.config.get('ai_analyzer.min_elixir'):,}")
        print(f"  Min Dark Elixir: {self.bot.config.get('ai_analyzer.min_dark_elixir'):,}")
        print("-" * 40)
        
        confirm = input("Confirm and start auto attack? (y/n): ").strip().lower()
        if confirm == 'y':
            # Pass the configured sessions to the bot
            self.bot.start_auto_attack(attack_sessions)
            print("\n✅ Auto attack started successfully!")
            print("Press Ctrl+Alt+S to stop at any time.")
        else:
            print("Auto attack cancelled.")

    def stop_auto_attack(self) -> None:
        """Stop the auto attack system"""
        if not self.bot.is_auto_attacking():
            print("Auto attack is not running")
            return
        
        print("Stopping auto attack...")
        self.bot.stop_auto_attack()
        print("Auto attack stopped")
    
    def show_auto_attack_stats(self) -> None:
        """Display auto attack statistics"""
        stats = self.bot.get_auto_attack_stats()
        
        print("\n" + "=" * 50)
        print("        AUTO ATTACK STATISTICS")
        print("=" * 50)
        print(f"Status: {'RUNNING' if stats['is_running'] else 'STOPPED'}")
        print(f"Total Attacks: {stats['total_attacks']}")
        print(f"Successful: {stats['successful_attacks']}")
        print(f"Failed: {stats['failed_attacks']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Runtime: {stats['runtime_hours']:.1f} hours")
        print(f"Attacks/Hour: {stats['attacks_per_hour']:.1f}")
        print(f"Last Attack: {stats['last_attack']}")
        print(f"Configured Sessions: {', '.join(stats['configured_sessions'])}")
        print("=" * 50)
        
        input("\nPress Enter to continue...")
    
    def configure_auto_attack_buttons(self) -> None:
        """Show required button mappings for auto attack"""
        required_buttons = self.bot.get_required_buttons()
        mapped_coords = self.bot.get_mapped_coordinates()
        
        print("\n" + "=" * 60)
        print("        REQUIRED BUTTON MAPPINGS")
        print("=" * 60)
        
        for button_name, description in required_buttons.items():
            status = "✓ MAPPED" if button_name in mapped_coords else "✗ MISSING"
            print(f"{button_name:20} | {status:10} | {description}")
        
        print("=" * 60)
        print("\nTo map missing buttons:")
        print("1. Go to 'Coordinate Mapping' in the main menu")
        print("2. Use F2 to record each button position")
        print("3. Use the exact button names shown above")
        
        input("\nPress Enter to continue...")

    def coordinate_mapping_menu(self) -> None:
        """Coordinate mapping submenu"""
        while True:
            print("\n" + "=" * 40)
            print("       COORDINATE MAPPING")
            print("=" * 40)
            print("1. Start coordinate mapping")
            print("2. View mapped coordinates")
            print("3. Export coordinates")
            print("4. Import coordinates")
            print("5. Back to main menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                print("\nStarting coordinate mapping mode...")
                print("Follow the on-screen instructions.")
                self.bot.start_coordinate_mapping()
            
            elif choice == '2':
                coords = self.bot.get_mapped_coordinates()
                if coords:
                    print("\n=== MAPPED COORDINATES ===")
                    for name, coord in coords.items():
                        print(f"  {name}: ({coord['x']}, {coord['y']})")
                else:
                    print("No coordinates mapped yet.")
            
            elif choice == '3':
                filename = input("Enter export filename (without extension): ").strip()
                if filename:
                    filepath = f"coordinates/{filename}.json"
                    self.bot.coordinate_mapper.export_coordinates(filepath)
            
            elif choice == '4':
                filename = input("Enter import filename: ").strip()
                if filename and os.path.exists(filename):
                    merge = input("Merge with existing coordinates? (y/n): ").strip().lower() == 'y'
                    self.bot.coordinate_mapper.import_coordinates(filename, merge)
                else:
                    print("File not found.")
            
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
    
    def attack_recording_menu(self) -> None:
        """Attack recording submenu"""
        while True:
            print("\n" + "=" * 40)
            print("       ATTACK RECORDING")
            print("=" * 40)
            auto_status = "ENABLED" if self.bot.attack_recorder.auto_detect_clicks else "DISABLED"
            print(f"Auto-detection: {auto_status}")
            print("=" * 40)
            print("1. Start new recording")
            print("2. List recordings")
            print("3. View recording info")
            print("4. Delete recording")
            print("5. Toggle auto-detection")
            print("6. Back to main menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                session_name = input("Enter session name: ").strip()
                if session_name:
                    self.bot.start_attack_recording(session_name)
                    input("\nPress Enter when recording is complete...")
                    self.bot.stop_attack_recording()
                else:
                    print("Session name required.")
            
            elif choice == '2':
                sessions = self.bot.list_recorded_attacks()
                if sessions:
                    print("\n=== RECORDED SESSIONS ===")
                    for i, session in enumerate(sessions, 1):
                        print(f"  {i}. {session}")
                else:
                    print("No recorded sessions found.")
            
            elif choice == '3':
                session_name = input("Enter session name: ").strip()
                if session_name:
                    info = self.bot.attack_recorder.get_recording_info(session_name)
                    if info:
                        print(f"\n=== SESSION INFO: {session_name} ===")
                        print(f"Created: {info['created']}")
                        print(f"Duration: {info['duration']:.1f} seconds")
                        print(f"Actions: {info['action_count']}")
                        print("Action types:")
                        for action_type, count in info['action_types'].items():
                            print(f"  {action_type}: {count}")
                    else:
                        print("Session not found.")
            
            elif choice == '4':
                session_name = input("Enter session name to delete: ").strip()
                if session_name:
                    confirm = input(f"Delete '{session_name}'? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.bot.attack_recorder.delete_recording(session_name)
            
            elif choice == '5':
                # Toggle auto-detection
                self.bot.attack_recorder.auto_detect_clicks = not self.bot.attack_recorder.auto_detect_clicks
                status = "ENABLED" if self.bot.attack_recorder.auto_detect_clicks else "DISABLED"
                print(f"🖱️ Auto-click detection is now {status}")
                if self.bot.attack_recorder.auto_detect_clicks:
                    print("✅ Clicks will be automatically recorded during sessions")
                    print("💡 If you get unwanted clicks, use F6 for manual mode instead")
                else:
                    print("⚠️ You must use F6 to manually record each click during sessions")
            
            elif choice == '6':
                break
            else:
                print("Invalid choice.")
    
    def attack_playback_menu(self) -> None:
        """Attack playback submenu"""
        while True:
            print("\n" + "=" * 40)
            print("       ATTACK PLAYBACK")
            print("=" * 40)
            print("1. Play attack")
            print("2. Preview recording")
            print("3. Validate recording")
            print("4. Set playback speed")
            print("5. Back to main menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                sessions = self.bot.list_recorded_attacks()
                if not sessions:
                    print("No recorded sessions available.")
                    continue
                
                print("\nAvailable sessions:")
                for i, session in enumerate(sessions, 1):
                    print(f"  {i}. {session}")
                
                try:
                    session_idx = int(input("Select session number: ")) - 1
                    if 0 <= session_idx < len(sessions):
                        session_name = sessions[session_idx]
                        speed = float(input("Playback speed (1.0 = normal): ") or "1.0")
                        
                        print(f"\nStarting playback of '{session_name}' at {speed}x speed")
                        print("Make sure COC is visible and in the correct state!")
                        input("Press Enter to begin...")
                        
                        self.bot.attack_player.play_attack(session_name, speed)
                        
                        # Wait for playback to complete
                        while self.bot.attack_player.is_playing:
                            time.sleep(0.5)
                    else:
                        print("Invalid session number.")
                except ValueError:
                    print("Invalid input.")
            
            elif choice == '2':
                session_name = input("Enter session name: ").strip()
                if session_name:
                    self.bot.attack_player.preview_recording(session_name)
            
            elif choice == '3':
                session_name = input("Enter session name: ").strip()
                if session_name:
                    validation = self.bot.attack_player.validate_recording(session_name)
                    print(f"\n=== VALIDATION RESULT ===")
                    print(f"Valid: {validation['valid']}")
                    print(f"Total actions: {validation['total_actions']}")
                    print(f"Duration: {validation['duration']:.1f} seconds")
                    
                    if not validation['valid']:
                        print(f"Error: {validation['error']}")
                        if validation.get('out_of_bounds'):
                            print("Out of bounds actions:")
                            for i, x, y in validation['out_of_bounds'][:5]:
                                print(f"  Action {i}: ({x}, {y})")
            
            elif choice == '4':
                try:
                    speed = float(input("Enter playback speed (0.1 - 5.0): "))
                    self.bot.attack_player.set_playback_speed(speed)
                except ValueError:
                    print("Invalid speed value.")
            
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
    
    def game_detection_menu(self) -> None:
        """Game detection submenu"""
        print("\n" + "=" * 40)
        print("       GAME DETECTION")
        print("=" * 40)
        
        print("Detecting COC game window...")
        bounds = self.bot.detect_game_window()
        
        if bounds:
            x, y, width, height = bounds
            print(f"Game window found!")
            print(f"Position: ({x}, {y})")
            print(f"Size: {width} x {height}")
            
            screenshot = input("\nTake screenshot of game window? (y/n): ").strip().lower()
            if screenshot == 'y':
                filepath = self.bot.take_screenshot(bounds)
                print(f"Screenshot saved: {filepath}")
        else:
            print("Game window not found.")
            print("Make sure Clash of Clans is running and visible.")
        
        input("\nPress Enter to continue...")
    
    def screenshots_menu(self) -> None:
        """Screenshots submenu"""
        while True:
            print("\n" + "=" * 40)
            print("         SCREENSHOTS")
            print("=" * 40)
            print("1. Take full screen screenshot")
            print("2. Take game window screenshot")
            print("3. View screenshots folder")
            print("4. Back to main menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                filepath = self.bot.take_screenshot()
                print(f"Screenshot saved: {filepath}")
            
            elif choice == '2':
                bounds = self.bot.detect_game_window()
                if bounds:
                    filepath = self.bot.take_screenshot(bounds)
                    print(f"Screenshot saved: {filepath}")
                else:
                    print("Game window not found.")
            
            elif choice == '3':
                screenshots_dir = "screenshots"
                if os.path.exists(screenshots_dir):
                    files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
                    if files:
                        print(f"\nScreenshots in {screenshots_dir}:")
                        for file in sorted(files)[-10:]:  # Show last 10
                            print(f"  {file}")
                        if len(files) > 10:
                            print(f"  ... and {len(files) - 10} more")
                    else:
                        print("No screenshots found.")
                else:
                    print("Screenshots directory not found.")
            
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
    
    def settings_menu(self) -> None:
        """Settings submenu"""
        print("\n" + "=" * 40)
        print("          SETTINGS")
        print("=" * 40)
        print("Current settings:")
        print("  PyAutoGUI Fail-safe: Enabled")
        print("  Screenshot format: PNG")
        print("  Default playback speed: 1.0x")
        print("\nSettings are currently read-only.")
        input("Press Enter to continue...")
    
    def show_help(self) -> None:
        """Display help information"""
        print("\n" + "=" * 60)
        print("                    HELP")
        print("=" * 60)
        print("""
GETTING STARTED:
1. Open Clash of Clans in full screen
2. Use 'Game Detection' to verify the bot can find your game
3. Map button coordinates for your screen resolution
4. Record attack sessions
5. Set up and start auto attack

COORDINATE MAPPING:
- Use F1 to start/stop mapping mode
- Move mouse to buttons and press F2 to record positions
- Press F3 to save coordinates
- ESC to cancel mapping

ATTACK RECORDING:
- Press F5 to start/stop recording
- Press F6 to manually record clicks
- Press F7 to add delays
- All mouse clicks are automatically recorded

ATTACK PLAYBACK:
- Press F8 to pause/resume during playback
- Press F9 to stop playback
- ESC for emergency stop

AUTO ATTACK SYSTEM - EXACT STRATEGY:
1. Click attack button
2. Click find_a_match to search for base  
3. Wait few seconds and take screenshot
4. Check enemy_gold, enemy_elixir, enemy_dark_elixir
5. If loot is good → start attack recording
6. If loot is bad → click next_button to skip
7. After attack starts → wait 3 minutes for battle
8. Click return_home button to go back
9. Repeat continuously
- Emergency stop: Ctrl+Alt+S

REQUIRED BUTTONS FOR AUTO ATTACK:
- attack: Main attack button on home screen
- find_a_match: Search for opponents
- next_button: Skip to next target
- return_home: Return to village after battle
- end_button: End battle button
- loot_1 through loot_8: Army slots (troops/spells for deployment)

OPTIONAL FOR LOOT CHECKING:
- enemy_gold: Enemy's gold display on attack screen
- enemy_elixir: Enemy's elixir display on attack screen
- enemy_dark_elixir: Enemy's dark elixir display on attack screen

TIPS:
- Make sure COC is in the same state when playing back
- Test recordings on practice attacks first
- Use slower speeds (0.5x) for more reliable playback
- Keep your screen resolution consistent
- Always supervise automation

SAFETY:
- Move mouse to top-left corner to trigger failsafe
- Use Ctrl+Alt+S for emergency stop during auto attack
- Always supervise bot operation
- Use at your own risk
        """)
        input("\nPress Enter to continue...") 