"""
Coordinate Mapper - Records and manages button coordinates for the COC bot
"""

import json
import os
import time
import pyautogui
import keyboard
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CoordinateMapper:
    """Records and manages button coordinates for automated clicking"""
    
    def __init__(self):
        self.coordinates_dir = "coordinates"
        self.coordinates_file = os.path.join(self.coordinates_dir, "button_coordinates.json")
        self.coordinates = {}
        self.is_mapping = False
        
        # Create coordinates directory
        os.makedirs(self.coordinates_dir, exist_ok=True)
        
        # Load existing coordinates
        self.load_coordinates()
        
        print("Coordinate Mapper initialized")
        print("Mapping Controls:")
        print("  F1 - Start/Stop coordinate mapping")
        print("  F2 - Record current mouse position")
        print("  F3 - Save coordinates")
        print("  ESC - Cancel mapping")
    
    def load_coordinates(self) -> None:
        """Load coordinates from file"""
        if os.path.exists(self.coordinates_file):
            try:
                with open(self.coordinates_file, 'r') as f:
                    self.coordinates = json.load(f)
                print(f"Loaded {len(self.coordinates)} coordinate mappings")
            except Exception as e:
                print(f"Error loading coordinates: {e}")
                self.coordinates = {}
        else:
            print("No existing coordinates file found")
    
    def save_coordinates(self, name: Optional[str] = None, coords: Optional[Dict] = None) -> None:
        """Save coordinates to file"""
        try:
            if coords:
                # Save specific coordinates
                if name:
                    self.coordinates[name] = coords
                else:
                    self.coordinates.update(coords)
            
            with open(self.coordinates_file, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            
            print(f"Coordinates saved to {self.coordinates_file}")
            print(f"Total mappings: {len(self.coordinates)}")
        except Exception as e:
            print(f"Error saving coordinates: {e}")
    
    def start_mapping(self) -> None:
        """Start interactive coordinate mapping"""
        if self.is_mapping:
            print("Already in mapping mode")
            return
        
        self.is_mapping = True
        current_session = {}
        
        print("\n=== COORDINATE MAPPING MODE ===")
        print("Instructions:")
        print("1. Move mouse to the button you want to map")
        print("2. Press F2 to record the position")
        print("3. Enter a name for the button")
        print("4. Repeat for all buttons")
        print("5. Press F3 to save all mappings")
        print("6. Press ESC to cancel")
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        try:
            while self.is_mapping:
                if keyboard.is_pressed('esc'):
                    print("\nMapping cancelled")
                    break
                
                if keyboard.is_pressed('f2'):
                    # Record current mouse position
                    x, y = pyautogui.position()
                    button_name = input(f"\nMouse at ({x}, {y}). Enter button name: ").strip()
                    
                    if button_name:
                        current_session[button_name] = {"x": x, "y": y}
                        print(f"Recorded '{button_name}' at ({x}, {y})")
                        print(f"Session mappings: {len(current_session)}")
                    
                    # Wait for key release
                    while keyboard.is_pressed('f2'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f3'):
                    # Save current session
                    if current_session:
                        self.coordinates.update(current_session)
                        self.save_coordinates()
                        print(f"\nSaved {len(current_session)} new mappings")
                        current_session.clear()
                    else:
                        print("\nNo mappings to save")
                    
                    # Wait for key release
                    while keyboard.is_pressed('f3'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f1'):
                    # Toggle mapping mode
                    print("\nExiting mapping mode")
                    break
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nMapping interrupted")
        
        finally:
            self.is_mapping = False
            print("Coordinate mapping stopped")
            
            # Save any remaining mappings
            if current_session:
                response = input(f"Save {len(current_session)} unsaved mappings? (y/n): ").strip().lower()
                if response == 'y':
                    self.coordinates.update(current_session)
                    self.save_coordinates()
    
    def get_coordinates(self, button_name: Optional[str] = None) -> Dict:
        """Get coordinates for a specific button or all buttons"""
        if button_name:
            return self.coordinates.get(button_name, {})
        return self.coordinates.copy()
    
    def add_coordinate(self, name: str, x: int, y: int) -> None:
        """Add a single coordinate mapping"""
        self.coordinates[name] = {"x": x, "y": y}
        print(f"Added coordinate '{name}' at ({x}, {y})")
    
    def remove_coordinate(self, name: str) -> bool:
        """Remove a coordinate mapping"""
        if name in self.coordinates:
            del self.coordinates[name]
            print(f"Removed coordinate '{name}'")
            return True
        else:
            print(f"Coordinate '{name}' not found")
            return False
    
    def list_coordinates(self) -> None:
        """Print all mapped coordinates"""
        if not self.coordinates:
            print("No coordinates mapped yet")
            return
        
        print("\n=== MAPPED COORDINATES ===")
        for name, coords in self.coordinates.items():
            print(f"  {name}: ({coords['x']}, {coords['y']})")
        print(f"Total: {len(self.coordinates)} mappings")
    
    def validate_coordinates(self) -> Dict[str, bool]:
        """Validate that all coordinates are within screen bounds"""
        screen_width, screen_height = pyautogui.size()
        validation = {}
        
        for name, coords in self.coordinates.items():
            x, y = coords['x'], coords['y']
            is_valid = 0 <= x < screen_width and 0 <= y < screen_height
            validation[name] = is_valid
            
            if not is_valid:
                print(f"WARNING: Coordinate '{name}' ({x}, {y}) is outside screen bounds")
        
        return validation
    
    def export_coordinates(self, filepath: str) -> None:
        """Export coordinates to a custom file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            print(f"Coordinates exported to {filepath}")
        except Exception as e:
            print(f"Error exporting coordinates: {e}")
    
    def import_coordinates(self, filepath: str, merge: bool = True) -> None:
        """Import coordinates from a file"""
        try:
            with open(filepath, 'r') as f:
                imported_coords = json.load(f)
            
            if merge:
                self.coordinates.update(imported_coords)
                print(f"Merged {len(imported_coords)} coordinates")
            else:
                self.coordinates = imported_coords
                print(f"Replaced with {len(imported_coords)} coordinates")
            
            self.save_coordinates()
        except Exception as e:
            print(f"Error importing coordinates: {e}") 