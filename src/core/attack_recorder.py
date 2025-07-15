"""
Attack Recorder - Records user attack sessions for later playback
"""

import json
import os
import time
import pyautogui
import keyboard
import threading
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class AttackRecorder:
    """Records attack sessions including mouse movements, clicks, and timing"""
    
    def __init__(self, auto_detect_clicks: bool = False):
        self.recordings_dir = "recordings"
        self.current_recording = []
        self.recording_thread = None
        self.is_recording = False
        self.start_time = None
        self.session_name = None
        self.auto_detect_clicks = auto_detect_clicks
        
        # Create recordings directory
        os.makedirs(self.recordings_dir, exist_ok=True)
        
        print("Attack Recorder initialized")
        print("Recording Controls:")
        print("  F5 - Start/Stop recording")
        print("  F6 - Record click at current position (MANUAL MODE)")
        print("  F7 - Add delay marker")
        print("  ESC - Cancel recording")
        if self.auto_detect_clicks:
            print("NOTE: Auto-click detection is ENABLED")
        else:
            print("NOTE: Auto-click detection is DISABLED (use F6 for manual recording)")
    
    def start_recording(self, session_name: str) -> None:
        """Start recording an attack session"""
        if self.is_recording:
            print("Already recording a session")
            return
        
        self.session_name = session_name
        self.current_recording = []
        self.is_recording = True
        self.start_time = time.time()
        
        print(f"\n=== RECORDING ATTACK SESSION: {session_name} ===")
        print("Instructions:")
        if self.auto_detect_clicks:
            print("1. Perform your attack as normal")
            print("2. All clicks will be recorded automatically")
            print("3. Press F7 to add delays between actions")
            print("4. Press F5 to stop recording")
            print("5. Press ESC to cancel")
            print("\nRECORDING STARTED - Auto-detection enabled...")
        else:
            print("1. Navigate to your attack position")
            print("2. Press F6 to record each click manually")
            print("3. Press F7 to add delays between actions")
            print("4. Press F5 to stop recording")
            print("5. Press ESC to cancel")
            print("\nRECORDING STARTED - Use F6 to record clicks...")
            print("(Auto-click detection is disabled)")
        
        # Start the recording thread
        self.recording_thread = threading.Thread(target=self._recording_loop)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def stop_recording(self) -> Optional[str]:
        """Stop the current recording and save it"""
        if not self.is_recording:
            print("No recording session active")
            return None
        
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=1)
        
        if self.current_recording:
            filepath = self._save_recording(self.session_name, self.current_recording)
            print(f"\nRecording saved: {filepath}")
            print(f"Total actions recorded: {len(self.current_recording)}")
            return filepath
        else:
            print("No actions recorded")
            return None
    
    def _recording_loop(self) -> None:
        """Main recording loop that captures user input"""
        last_mouse_pos = pyautogui.position()
        
        try:
            while self.is_recording:
                current_time = time.time() - self.start_time
                
                # Check for manual recording hotkeys
                if keyboard.is_pressed('esc'):
                    print("\nRecording cancelled")
                    self.is_recording = False
                    break
                
                if keyboard.is_pressed('f5'):
                    print("\nStopping recording")
                    self.is_recording = False
                    break
                
                if keyboard.is_pressed('f6'):
                    # Manual click recording
                    x, y = pyautogui.position()
                    self._add_action('click', x, y, current_time)
                    print(f"Recorded click at ({x}, {y})")
                    
                    # Wait for key release
                    while keyboard.is_pressed('f6'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f7'):
                    # Add delay marker
                    delay = float(input("\nEnter delay in seconds: ") or "1.0")
                    self._add_action('delay', 0, 0, current_time, {'duration': delay})
                    print(f"Added {delay}s delay")
                    
                    # Wait for key release
                    while keyboard.is_pressed('f7'):
                        time.sleep(0.1)
                
                # Optional auto-detection (disabled by default)
                if self.auto_detect_clicks:
                    try:
                        # Use win32 API for more reliable mouse detection
                        import win32api
                        left_button_state = win32api.GetKeyState(0x01)  # VK_LBUTTON
                        if left_button_state < 0:  # Button is pressed
                            x, y = pyautogui.position()
                            # Check if this is a new click (avoid duplicates)
                            if not hasattr(self, '_last_click_time') or (current_time - self._last_click_time) > 0.1:
                                self._add_action('click', x, y, current_time)
                                print(f"Auto-recorded click at ({x}, {y})")
                                self._last_click_time = current_time
                    except:
                        # If auto-detection fails, just continue
                        pass
                
                # Track significant mouse movements
                current_mouse_pos = pyautogui.position()
                if self._distance(last_mouse_pos, current_mouse_pos) > 50:
                    self._add_action('move', current_mouse_pos[0], current_mouse_pos[1], current_time)
                    last_mouse_pos = current_mouse_pos
                
                time.sleep(0.05)  # 20 FPS recording
        
        except Exception as e:
            print(f"Recording error: {e}")
            self.is_recording = False
    
    def _add_action(self, action_type: str, x: int, y: int, timestamp: float, extra_data: Optional[Dict] = None) -> None:
        """Add an action to the current recording"""
        action = {
            'type': action_type,
            'x': x,
            'y': y,
            'timestamp': timestamp,
            'relative_time': timestamp
        }
        
        if extra_data:
            action.update(extra_data)
        
        self.current_recording.append(action)
    
    def _distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate distance between two points"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def _save_recording(self, name: str, recording: List[Dict]) -> str:
        """Save a recording to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = os.path.join(self.recordings_dir, filename)
        
        recording_data = {
            'name': name,
            'created': datetime.now().isoformat(),
            'duration': recording[-1]['timestamp'] if recording else 0,
            'actions': recording
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(recording_data, f, indent=2)
            return filepath
        except Exception as e:
            print(f"Error saving recording: {e}")
            return ""
    
    def list_sessions(self) -> List[str]:
        """Get list of all recorded sessions"""
        if not os.path.exists(self.recordings_dir):
            return []
        
        sessions = []
        for file in os.listdir(self.recordings_dir):
            if file.endswith('.json'):
                sessions.append(file[:-5])  # Remove .json extension
        
        return sorted(sessions)
    
    def load_recording(self, session_name: str) -> Optional[Dict]:
        """Load a recording by name"""
        filepath = os.path.join(self.recordings_dir, f"{session_name}.json")
        
        if not os.path.exists(filepath):
            print(f"Recording not found: {session_name}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading recording: {e}")
            return None
    
    def delete_recording(self, session_name: str) -> bool:
        """Delete a recording"""
        filepath = os.path.join(self.recordings_dir, f"{session_name}.json")
        
        if not os.path.exists(filepath):
            print(f"Recording not found: {session_name}")
            return False
        
        try:
            os.remove(filepath)
            print(f"Deleted recording: {session_name}")
            return True
        except Exception as e:
            print(f"Error deleting recording: {e}")
            return False
    
    def get_recording_info(self, session_name: str) -> Optional[Dict]:
        """Get information about a recording"""
        recording = self.load_recording(session_name)
        if not recording:
            return None
        
        return {
            'name': recording.get('name', session_name),
            'created': recording.get('created', 'Unknown'),
            'duration': recording.get('duration', 0),
            'action_count': len(recording.get('actions', [])),
            'action_types': self._count_action_types(recording.get('actions', []))
        }
    
    def _count_action_types(self, actions: List[Dict]) -> Dict[str, int]:
        """Count the types of actions in a recording"""
        counts = {}
        for action in actions:
            action_type = action.get('type', 'unknown')
            counts[action_type] = counts.get(action_type, 0) + 1
        return counts 