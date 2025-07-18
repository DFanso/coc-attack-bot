"""
Config - Configuration management for the COC Attack Bot
"""

import json
import os
from typing import Dict, Any, Optional

class Config:
    """Configuration management for the COC Attack Bot"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
        
        # Load existing config if it exists
        if os.path.exists(config_file):
            self.load_config()
        else:
            self.save_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "bot": {
                "name": "COC Attack Bot",
                "version": "1.0.0",
                "author": "COC Bot User"
            },
            "automation": {
                "default_click_delay": 0.1,
                "default_playback_speed": 1.0,
                "screenshot_format": "PNG",
                "failsafe_enabled": True,
                "max_recording_duration": 300,  # 5 minutes
                "auto_save_recordings": True
            },
            "display": {
                "show_coordinates_on_click": True,
                "show_progress_during_playback": True,
                "log_level": "INFO"
            },
            "directories": {
                "screenshots": "screenshots",
                "recordings": "recordings",
                "coordinates": "coordinates",
                "templates": "templates",
                "logs": "logs"
            },
            "hotkeys": {
                "coordinate_mapping": {
                    "start_stop": "f1",
                    "record_position": "f2",
                    "save_coordinates": "f3",
                    "cancel": "esc"
                },
                "recording": {
                    "start_stop": "f5",
                    "manual_click": "f6",
                    "add_delay": "f7",
                    "cancel": "esc"
                },
                "playback": {
                    "pause_resume": "f8",
                    "stop": "f9",
                    "emergency_stop": "esc"
                }
            },
            "game": {
                "window_titles": [
                    "Clash of Clans",
                    "BlueStacks",
                    "NoxPlayer",
                    "LDPlayer",
                    "MEmu"
                ],
                "detection_timeout": 10,
                "click_precision": 5,  # pixels
                "template_matching_threshold": 0.8
            },
            "ai_analyzer": {
                "google_gemini_api_key": "AIzaSyC5tOcA2F_HA20BvrDMLlS7UDyFuT",
                "enabled": False,
                "min_gold": 300000,
                "min_elixir": 300000,
                "min_dark_elixir": 2000
            }
        }
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            self._merge_config(self.config, loaded_config)
            
            print(f"Configuration loaded from {self.config_file}")
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_config(self, default: Dict, loaded: Dict) -> None:
        """Recursively merge loaded config with defaults"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value by dot-separated key path"""
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
    
    def get_hotkey(self, category: str, action: str) -> str:
        """Get hotkey for specific action"""
        return self.get(f"hotkeys.{category}.{action}", "")
    
    def get_directory(self, name: str) -> str:
        """Get directory path"""
        return self.get(f"directories.{name}", name)
    
    def get_click_delay(self) -> float:
        """Get default click delay"""
        return self.get("automation.default_click_delay", 0.1)
    
    def get_playback_speed(self) -> float:
        """Get default playback speed"""
        return self.get("automation.default_playback_speed", 1.0)
    
    def is_failsafe_enabled(self) -> bool:
        """Check if failsafe is enabled"""
        return self.get("automation.failsafe_enabled", True)
    
    def get_game_window_titles(self) -> list:
        """Get list of game window titles to search for"""
        return self.get("game.window_titles", ["Clash of Clans"])
    
    def get_template_threshold(self) -> float:
        """Get template matching threshold"""
        return self.get("game.template_matching_threshold", 0.8)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self.config = self._load_default_config()
        self.save_config()
        print("Configuration reset to defaults")
    
    def update_bot_info(self, name: Optional[str] = None, version: Optional[str] = None, author: Optional[str] = None) -> None:
        """Update bot information"""
        if name:
            self.set("bot.name", name)
        if version:
            self.set("bot.version", version)
        if author:
            self.set("bot.author", author)
        
        self.save_config()
    
    def print_config(self) -> None:
        """Print current configuration"""
        print("\n=== CURRENT CONFIGURATION ===")
        print(json.dumps(self.config, indent=2))
    
    def export_config(self, filepath: str) -> bool:
        """Export configuration to a file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"Configuration exported to {filepath}")
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False 