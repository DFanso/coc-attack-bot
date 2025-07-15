#!/usr/bin/env python3
"""
Example Usage - Demonstrates how to use the COC Attack Bot programmatically
"""

import time
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bot_controller import BotController

def example_coordinate_mapping():
    """Example of programmatic coordinate mapping"""
    print("=== EXAMPLE: Coordinate Mapping ===")
    
    bot = BotController()
    
    # Add some example coordinates (you would get these from actual mouse positions)
    example_coords = {
        "attack_button": {"x": 100, "y": 200},
        "army_camp": {"x": 150, "y": 250},
        "barbarian": {"x": 200, "y": 300},
        "archer": {"x": 250, "y": 300},
        "spell_button": {"x": 300, "y": 350}
    }
    
    # Save the coordinates
    for name, coords in example_coords.items():
        bot.coordinate_mapper.add_coordinate(name, coords["x"], coords["y"])
    
    # Save to file
    bot.coordinate_mapper.save_coordinates()
    
    # List all coordinates
    bot.coordinate_mapper.list_coordinates()

def example_screenshot():
    """Example of taking screenshots"""
    print("\n=== EXAMPLE: Screenshot Capture ===")
    
    bot = BotController()
    
    # Detect game window
    bounds = bot.detect_game_window()
    if bounds:
        print(f"Game window detected: {bounds}")
        
        # Take a screenshot of the game window
        screenshot_path = bot.take_screenshot(bounds)
        print(f"Game screenshot saved: {screenshot_path}")
    else:
        print("Game window not found - taking full screen screenshot")
        screenshot_path = bot.take_screenshot()
        print(f"Full screen screenshot saved: {screenshot_path}")

def example_recording_info():
    """Example of working with recording information"""
    print("\n=== EXAMPLE: Recording Information ===")
    
    bot = BotController()
    
    # List all recorded sessions
    sessions = bot.list_recorded_attacks()
    if sessions:
        print("Available recorded sessions:")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")
            
            # Get detailed info about the first session
            if i == 1:
                info = bot.attack_recorder.get_recording_info(session)
                if info:
                    print(f"\nDetails for '{session}':")
                    print(f"  Created: {info['created']}")
                    print(f"  Duration: {info['duration']:.1f} seconds")
                    print(f"  Actions: {info['action_count']}")
                    print("  Action types:")
                    for action_type, count in info['action_types'].items():
                        print(f"    {action_type}: {count}")
    else:
        print("No recorded sessions found.")
        print("Use the main application to record attack sessions first.")

def example_config_usage():
    """Example of working with configuration"""
    print("\n=== EXAMPLE: Configuration ===")
    
    bot = BotController()
    
    # Get some configuration values
    click_delay = bot.config.get_click_delay()
    playback_speed = bot.config.get_playback_speed()
    failsafe = bot.config.is_failsafe_enabled()
    
    print(f"Click delay: {click_delay}s")
    print(f"Playback speed: {playback_speed}x")
    print(f"Failsafe enabled: {failsafe}")
    
    # Get hotkey mappings
    record_hotkey = bot.config.get_hotkey("recording", "start_stop")
    click_hotkey = bot.config.get_hotkey("recording", "manual_click")
    
    print(f"Record hotkey: {record_hotkey}")
    print(f"Manual click hotkey: {click_hotkey}")

def main():
    """Main example function"""
    print("COC Attack Bot - Example Usage")
    print("=" * 50)
    
    try:
        # Run examples
        example_coordinate_mapping()
        example_screenshot()
        example_recording_info()
        example_config_usage()
        
        print("\n" + "=" * 50)
        print("Examples completed successfully!")
        print("\nTo use the full interactive interface, run:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\nExample error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main() 