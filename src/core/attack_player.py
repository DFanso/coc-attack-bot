"""
Attack Player - Plays back recorded attack sessions
"""

import json
import time
import pyautogui
import keyboard
import threading
from typing import Dict, List, Optional
from .attack_recorder import AttackRecorder

class AttackPlayer:
    """Plays back recorded attack sessions"""
    
    def __init__(self):
        self.attack_recorder = AttackRecorder()
        self.is_playing = False
        self.current_playback = None
        self.playback_thread = None
        self.playback_speed = 1.0
        
        print("Attack Player initialized")
        print("Playback Controls:")
        print("  F8 - Pause/Resume playback")
        print("  F9 - Stop playback")
        print("  ESC - Emergency stop")
    
    def play_attack(self, session_name: str, speed: float = 1.0) -> bool:
        """Play back a recorded attack session"""
        if self.is_playing:
            print("Already playing an attack")
            return False
        
        # Load the recording
        recording = self.attack_recorder.load_recording(session_name)
        if not recording:
            print(f"Could not load recording: {session_name}")
            return False
        
        self.current_playback = recording
        self.playback_speed = speed
        self.is_playing = True
        
        print(f"\n=== PLAYING ATTACK SESSION: {session_name} ===")
        print(f"Duration: {recording.get('duration', 0):.1f} seconds")
        print(f"Actions: {len(recording.get('actions', []))}")
        print(f"Speed: {speed}x")
        print("\nStarting playback in 3 seconds...")
        print("Press F8 to pause, F9 to stop, ESC for emergency stop")
        
        time.sleep(3)
        
        # Start playback thread
        self.playback_thread = threading.Thread(
            target=self._playback_loop, 
            args=(recording.get('actions', []),)
        )
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
        return True
    
    def stop_playback(self) -> None:
        """Stop the current playback"""
        if not self.is_playing:
            print("No playback active")
            return
        
        print("Stopping playback")
        self.is_playing = False
        
        if self.playback_thread:
            self.playback_thread.join(timeout=2)
    
    def _playback_loop(self, actions: List[Dict]) -> None:
        """Main playback loop"""
        try:
            last_timestamp = 0
            paused = False
            
            for i, action in enumerate(actions):
                if not self.is_playing:
                    break
                
                # Check for control keys
                if keyboard.is_pressed('esc'):
                    print("\nEmergency stop activated")
                    break
                
                if keyboard.is_pressed('f9'):
                    print("\nPlayback stopped by user")
                    break
                
                if keyboard.is_pressed('f8'):
                    paused = not paused
                    status = "paused" if paused else "resumed"
                    print(f"\nPlayback {status}")
                    
                    # Wait for key release
                    while keyboard.is_pressed('f8'):
                        time.sleep(0.1)
                
                # Handle pause
                while paused and self.is_playing:
                    time.sleep(0.1)
                    if keyboard.is_pressed('f8'):
                        paused = False
                        print("Playback resumed")
                        while keyboard.is_pressed('f8'):
                            time.sleep(0.1)
                
                if not self.is_playing:
                    break
                
                # Calculate delay based on timestamps
                current_timestamp = action.get('timestamp', 0)
                if i > 0:
                    delay = (current_timestamp - last_timestamp) / self.playback_speed
                    if delay > 0:
                        time.sleep(delay)
                
                # Execute the action
                self._execute_action(action)
                last_timestamp = current_timestamp
                
                # Progress indicator
                progress = (i + 1) / len(actions) * 100
                print(f"\rProgress: {progress:.1f}% ({i + 1}/{len(actions)})", end='', flush=True)
        
        except Exception as e:
            print(f"\nPlayback error: {e}")
        
        finally:
            self.is_playing = False
            print(f"\nPlayback completed")
    
    def _execute_action(self, action: Dict) -> None:
        """Execute a single action"""
        action_type = action.get('type', '')
        x = action.get('x', 0)
        y = action.get('y', 0)
        
        try:
            if action_type == 'click':
                pyautogui.click(x, y)
                print(f" - Click at ({x}, {y})")
            
            elif action_type == 'move':
                pyautogui.moveTo(x, y)
                print(f" - Move to ({x}, {y})")
            
            elif action_type == 'delay':
                duration = action.get('duration', 1.0) / self.playback_speed
                time.sleep(duration)
                print(f" - Delay {duration:.1f}s")
            
            elif action_type == 'drag':
                start_x = action.get('start_x', x)
                start_y = action.get('start_y', y)
                pyautogui.drag(x - start_x, y - start_y, duration=0.5)
                print(f" - Drag from ({start_x}, {start_y}) to ({x}, {y})")
            
            else:
                print(f" - Unknown action: {action_type}")
        
        except Exception as e:
            print(f" - Error executing action {action_type}: {e}")
    
    def validate_recording(self, session_name: str) -> Dict[str, any]:
        """Validate a recording before playback"""
        recording = self.attack_recorder.load_recording(session_name)
        if not recording:
            return {'valid': False, 'error': 'Recording not found'}
        
        actions = recording.get('actions', [])
        if not actions:
            return {'valid': False, 'error': 'No actions in recording'}
        
        # Check screen bounds
        screen_width, screen_height = pyautogui.size()
        out_of_bounds = []
        
        for i, action in enumerate(actions):
            x, y = action.get('x', 0), action.get('y', 0)
            if not (0 <= x < screen_width and 0 <= y < screen_height):
                out_of_bounds.append((i, x, y))
        
        result = {
            'valid': len(out_of_bounds) == 0,
            'total_actions': len(actions),
            'duration': recording.get('duration', 0),
            'out_of_bounds': out_of_bounds
        }
        
        if out_of_bounds:
            result['error'] = f"{len(out_of_bounds)} actions are out of screen bounds"
        
        return result
    
    def preview_recording(self, session_name: str) -> None:
        """Show a preview of the recording actions"""
        recording = self.attack_recorder.load_recording(session_name)
        if not recording:
            print(f"Recording not found: {session_name}")
            return
        
        actions = recording.get('actions', [])
        
        print(f"\n=== RECORDING PREVIEW: {session_name} ===")
        print(f"Duration: {recording.get('duration', 0):.1f} seconds")
        print(f"Total actions: {len(actions)}")
        
        # Show action summary
        action_counts = {}
        for action in actions:
            action_type = action.get('type', 'unknown')
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        print("\nAction breakdown:")
        for action_type, count in action_counts.items():
            print(f"  {action_type}: {count}")
        
        # Show first few actions
        print(f"\nFirst 10 actions:")
        for i, action in enumerate(actions[:10]):
            timestamp = action.get('timestamp', 0)
            action_type = action.get('type', 'unknown')
            x, y = action.get('x', 0), action.get('y', 0)
            print(f"  {i+1:2d}. {timestamp:6.1f}s - {action_type} at ({x}, {y})")
        
        if len(actions) > 10:
            print(f"  ... and {len(actions) - 10} more actions")
    
    def set_playback_speed(self, speed: float) -> None:
        """Set the playback speed multiplier"""
        if speed <= 0:
            print("Speed must be positive")
            return
        
        self.playback_speed = speed
        print(f"Playback speed set to {speed}x") 