"""
Auto Attacker - Automated continuous attack system for COC
"""

import time
import random
import threading
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pyautogui
import keyboard

from .attack_player import AttackPlayer
from .screen_capture import ScreenCapture
from .coordinate_mapper import CoordinateMapper
from ..utils.logger import Logger

class AutoAttacker:
    """Automated continuous attack system"""
    
    def __init__(self, attack_player: AttackPlayer, screen_capture: ScreenCapture, 
                 coordinate_mapper: CoordinateMapper, logger: Logger):
        self.attack_player = attack_player
        self.screen_capture = screen_capture
        self.coordinate_mapper = CoordinateMapper()
        self.logger = logger
        
        self.is_running = False
        self.auto_thread = None
        self.stats = {
            'total_attacks': 0,
            'successful_attacks': 0,
            'failed_attacks': 0,
            'start_time': None,
            'last_attack_time': None
        }
        
        # Configuration
        self.config = {
            'attack_sessions': [],  # List of attack sessions to rotate
            'army_wait_time': 1800,  # 30 minutes default army training time
            'search_timeout': 120,   # 2 minutes to find target
            'max_search_attempts': 10,
            'attack_delay_min': 30,  # Min seconds between attacks
            'attack_delay_max': 60,  # Max seconds between attacks
            'return_home_timeout': 30,
            'check_army_interval': 300,  # Check army every 5 minutes
            'skip_army_check': True,  # Skip army waiting completely (default enabled)
        }
        
        self.logger.info("Auto Attacker initialized")
    
    def add_attack_session(self, session_name: str) -> bool:
        """Add an attack session to the rotation"""
        if session_name not in self.config['attack_sessions']:
            self.config['attack_sessions'].append(session_name)
            self.logger.info(f"Added attack session: {session_name}")
            return True
        return False
    
    def remove_attack_session(self, session_name: str) -> bool:
        """Remove an attack session from rotation"""
        if session_name in self.config['attack_sessions']:
            self.config['attack_sessions'].remove(session_name)
            self.logger.info(f"Removed attack session: {session_name}")
            return True
        return False
    
    def set_army_wait_time(self, minutes: int) -> None:
        """Set army training wait time in minutes"""
        self.config['army_wait_time'] = minutes * 60
        self.logger.info(f"Army wait time set to {minutes} minutes")
    
    def set_skip_army_check(self, skip: bool) -> None:
        """Enable/disable army checking - skip means attack immediately"""
        self.config['skip_army_check'] = skip
        status = "DISABLED" if skip else "ENABLED"
        self.logger.info(f"Army checking {status}")
    
    def start_auto_attack(self) -> bool:
        """Start the automated attack loop"""
        if self.is_running:
            self.logger.warning("Auto attacker is already running")
            return False
        
        if not self.config['attack_sessions']:
            self.logger.error("No attack sessions configured")
            return False
        
        # Verify attack sessions exist
        for session in self.config['attack_sessions']:
            if not self.attack_player.attack_recorder.load_recording(session):
                self.logger.error(f"Attack session not found: {session}")
                return False
        
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        self.stats['total_attacks'] = 0
        self.stats['successful_attacks'] = 0
        self.stats['failed_attacks'] = 0
        
        # Start the automation thread
        self.auto_thread = threading.Thread(target=self._auto_attack_loop, daemon=True)
        self.auto_thread.start()
        
        self.logger.info("Auto attacker started")
        return True
    
    def stop_auto_attack(self) -> None:
        """Stop the automated attack loop"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.logger.info("Auto attacker stopping...")
        
        if self.auto_thread:
            self.auto_thread.join(timeout=5)
        
        self.logger.info("Auto attacker stopped")
        self._print_stats()
    
    def _auto_attack_loop(self) -> None:
        """Main automation loop"""
        try:
            while self.is_running:
                # Check for emergency stop
                if keyboard.is_pressed('ctrl+alt+s'):
                    self.logger.info("Emergency stop activated (Ctrl+Alt+S)")
                    break
                
                # Ensure we're at home base
                if not self._ensure_home_base():
                    self.logger.error("Could not return to home base")
                    time.sleep(30)
                    continue
                
                # Check if army is ready (skip if configured)
                if not self.config['skip_army_check']:
                    if not self._check_army_ready():
                        self.logger.info("Army not ready, waiting...")
                        self._wait_for_army()
                        continue
                else:
                    self.logger.info("Army check skipped - attacking immediately")
                
                # Start attack sequence
                attack_success = self._execute_attack_sequence()
                
                # Update statistics
                self.stats['total_attacks'] += 1
                if attack_success:
                    self.stats['successful_attacks'] += 1
                else:
                    self.stats['failed_attacks'] += 1
                
                self.stats['last_attack_time'] = datetime.now()
                
                # Wait between attacks
                delay = random.randint(
                    self.config['attack_delay_min'], 
                    self.config['attack_delay_max']
                )
                self.logger.info(f"Waiting {delay} seconds before next attack...")
                
                for _ in range(delay):
                    if not self.is_running:
                        break
                    time.sleep(1)
        
        except Exception as e:
            self.logger.error(f"Auto attack loop error: {e}")
        finally:
            self.is_running = False
    
    def _ensure_home_base(self) -> bool:
        """Ensure we're at the home base"""
        coords = self.coordinate_mapper.get_coordinates()
        
        # Try to click home button if mapped
        if 'end_button' in coords:
            home_coord = coords['end_button']
            pyautogui.click(home_coord['x'], home_coord['y'])
            time.sleep(2)
            return True
        
        # Alternative: Look for home indicators
        # This would use template matching to find home screen elements
        self.logger.warning("Home button not mapped, assuming at home base")
        return True
    
    def _check_army_ready(self) -> bool:
        """Check if army is ready for attack"""
        # If skip army check is enabled, always return True
        if self.config['skip_army_check']:
            return True
            
        coords = self.coordinate_mapper.get_coordinates()
        
        # Check army camps if mapped
        if 'army_camp' in coords:
            # Take screenshot and analyze army status
            # For now, we'll use a simple approach
            pass
        
        # Placeholder: Always return True for now
        # In a real implementation, this would check army capacity
        self.logger.info("Checking army status...")
        return True
    
    def _wait_for_army(self) -> None:
        """Wait for army to be ready"""
        wait_time = self.config['army_wait_time']
        self.logger.info(f"Waiting {wait_time//60} minutes for army to train...")
        
        # Wait in chunks to allow stopping
        for _ in range(wait_time):
            if not self.is_running:
                break
            time.sleep(1)
    
    def _execute_attack_sequence(self) -> bool:
        """Execute a complete attack sequence"""
        try:
            # Step 1: Find a target
            if not self._find_target():
                self.logger.warning("Could not find suitable target")
                return False
            
            # Step 2: Execute attack
            session_name = self._get_next_attack_session()
            self.logger.info(f"Executing attack: {session_name}")
            
            # Play the attack
            if not self.attack_player.play_attack(session_name, speed=1.0):
                self.logger.error("Failed to start attack playback")
                return False
            
            # Wait for attack to complete
            while self.attack_player.is_playing and self.is_running:
                time.sleep(1)
            
            # Step 3: Wait for battle to end
            time.sleep(10)  # Wait for battle results
            
            # Step 4: Return home
            self._return_home()
            
            self.logger.info("Attack sequence completed successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Attack sequence failed: {e}")
            return False
    
    def _find_target(self) -> bool:
        """Find a suitable target to attack"""
        coords = self.coordinate_mapper.get_coordinates()
        
        # Click attack button
        if 'attack' in coords:
            attack_coord = coords['attack']
            pyautogui.click(attack_coord['x'], attack_coord['y'])
            time.sleep(2)
        else:
            self.logger.error("Attack button not mapped")
            return False
        
        # Search for targets
        search_attempts = 0
        max_attempts = self.config['max_search_attempts']
        
        while search_attempts < max_attempts and self.is_running:
            # Click find match or next button to search for targets
            if 'find_a_match' in coords:
                find_coord = coords['find_a_match']
                pyautogui.click(find_coord['x'], find_coord['y'])
                time.sleep(3)
                # Accept first target found - attack immediately
                return True
            elif 'next_button' in coords:
                # If no find_a_match, try next button to skip targets
                next_coord = coords['next_button']
                pyautogui.click(next_coord['x'], next_coord['y'])
                time.sleep(2)
            
            search_attempts += 1
            time.sleep(2)
        
        self.logger.warning(f"Could not find target after {max_attempts} attempts")
        return False
    
    def _get_next_attack_session(self) -> str:
        """Get the next attack session to use"""
        if not self.config['attack_sessions']:
            return ""
        
        # Rotate through attack sessions
        session_index = self.stats['total_attacks'] % len(self.config['attack_sessions'])
        return self.config['attack_sessions'][session_index]
    
    def _return_home(self) -> None:
        """Return to home base after attack"""
        coords = self.coordinate_mapper.get_coordinates()
        
        # Click return home or end battle button
        if 'return_home' in coords:
            home_coord = coords['return_home']
            pyautogui.click(home_coord['x'], home_coord['y'])
            time.sleep(3)
        
        # Click end button to finish battle
        if 'end_button' in coords:
            end_coord = coords['end_button']
            pyautogui.click(end_coord['x'], end_coord['y'])
            time.sleep(2)
    
    def get_stats(self) -> Dict:
        """Get automation statistics"""
        if self.stats['start_time']:
            runtime = datetime.now() - self.stats['start_time']
            runtime_hours = runtime.total_seconds() / 3600
        else:
            runtime_hours = 0
        
        return {
            'is_running': self.is_running,
            'total_attacks': self.stats['total_attacks'],
            'successful_attacks': self.stats['successful_attacks'],
            'failed_attacks': self.stats['failed_attacks'],
            'success_rate': (self.stats['successful_attacks'] / max(self.stats['total_attacks'], 1)) * 100,
            'runtime_hours': runtime_hours,
            'attacks_per_hour': self.stats['total_attacks'] / max(runtime_hours, 1),
            'last_attack': self.stats['last_attack_time'].strftime("%H:%M:%S") if self.stats['last_attack_time'] else "None",
            'configured_sessions': self.config['attack_sessions'].copy()
        }
    
    def _print_stats(self) -> None:
        """Print automation statistics"""
        stats = self.get_stats()
        print("\n" + "=" * 50)
        print("        AUTO ATTACKER STATISTICS")
        print("=" * 50)
        print(f"Total Attacks: {stats['total_attacks']}")
        print(f"Successful: {stats['successful_attacks']}")
        print(f"Failed: {stats['failed_attacks']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Runtime: {stats['runtime_hours']:.1f} hours")
        print(f"Attacks/Hour: {stats['attacks_per_hour']:.1f}")
        print(f"Last Attack: {stats['last_attack']}")
        print("=" * 50)
    
    def configure_buttons(self) -> Dict[str, str]:
        """Get list of required button mappings"""
        return {
            'attack': 'Main attack button on home screen',
            'find_a_match': 'Find match/search button',
            'next_button': 'Next/search for another target',
            'return_home': 'Return home after battle',
            'end_button': 'End battle button',
            'loot_1': 'First army slot (optional)',
            'army_camp': 'Army camp to check troop status (optional)'
        } 