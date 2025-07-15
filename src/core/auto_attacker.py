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
            'max_search_attempts': 10,
            'min_gold': 100000,  # Minimum gold required
            'min_elixir': 100000,  # Minimum elixir required
            'min_dark_elixir': 1000,  # Minimum dark elixir required
        }
        
        self.current_session_index = 0
        
        print("Auto Attacker initialized")
        print("Emergency stop: Ctrl+Alt+S")
    
    def add_attack_session(self, session_name: str) -> bool:
        """Add an attack session to rotation"""
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
    
    def start_auto_attack(self) -> None:
        """Start the automated attack system"""
        if self.is_running:
            print("Auto attacker already running")
            return
        
        if not self.config['attack_sessions']:
            self.logger.error("No attack sessions configured. Please add at least one session.")
            return
        
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        
        self.auto_thread = threading.Thread(target=self._auto_attack_loop)
        self.auto_thread.daemon = True
        self.auto_thread.start()
        
        self.logger.info("Auto attacker started")
    
    def stop_auto_attack(self) -> None:
        """Stop the automated attack system"""
        if not self.is_running:
            return
        
        self.logger.info("Auto attacker stopping...")
        self.is_running = False
        
        # Stop any playing attack
        self.attack_player.stop_playback()
        
        if self.auto_thread and self.auto_thread.is_alive():
            self.auto_thread.join(timeout=5)
        
        self.logger.info("Auto attacker stopped")
    
    def _auto_attack_loop(self) -> None:
        """Main automation loop"""
        try:
            while self.is_running:
                # Check emergency stop
                if keyboard.is_pressed('ctrl+alt+s'):
                    self.logger.warning("Emergency stop activated!")
                    break
                
                self.logger.info("🎯 Starting new attack cycle...")
                
                # Execute attack sequence
                if self._execute_attack_sequence():
                    self.stats['successful_attacks'] += 1
                    self.logger.info("✅ Attack sequence completed successfully")
                else:
                    self.stats['failed_attacks'] += 1
                    self.logger.warning("❌ Attack sequence failed")
                
                self.stats['total_attacks'] += 1
                self.stats['last_attack_time'] = datetime.now()
                
                # Short break between attacks
                if self.is_running:
                    delay = random.randint(5, 15)
                    self.logger.info(f"⏳ Waiting {delay} seconds before next attack...")
                    time.sleep(delay)
                    
        except Exception as e:
            self.logger.error(f"Auto attack loop error: {e}")
        finally:
            self.is_running = False
    
    def _execute_attack_sequence(self) -> bool:
        """Execute the complete attack sequence following your exact process"""
        try:
            coords = self.coordinate_mapper.get_coordinates()
            
            # Step 1: Click attack button
            if 'attack' not in coords:
                self.logger.error("Attack button not mapped")
                return False
                
            attack_coord = coords['attack']
            self.logger.info(f"1️⃣ Clicking attack button at ({attack_coord['x']}, {attack_coord['y']})")
            pyautogui.click(attack_coord['x'], attack_coord['y'])
            time.sleep(2)  # Wait for attack screen
            
            # Step 2-6: Find good loot target
            if not self._find_good_loot_target():
                self.logger.warning("Could not find good loot target")
                return False
            
            # Step 7: Start attack recording (only after good loot found)
            session_name = self._get_next_attack_session()
            self.logger.info(f"🎯 Starting attack with session: {session_name}")
            
            if not self.attack_player.play_attack(session_name, speed=1.0):
                self.logger.error("Failed to start attack recording")
                return False
            
            self.logger.info("✅ Attack recording started - troops deploying...")
            
            # Step 8: Wait 3 minutes for battle completion
            self.logger.info("⏳ Waiting 3 minutes for battle completion...")
            battle_wait_time = 180  # 3 minutes
            
            for remaining in range(battle_wait_time, 0, -10):
                if not self.is_running:
                    break
                self.logger.info(f"⏳ Battle in progress... {remaining//60}m {remaining%60}s remaining")
                time.sleep(10)
            
            # Step 9: Return home
            self._return_home()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Attack sequence failed: {e}")
            return False
    
    def _find_good_loot_target(self) -> bool:
        """Find target with good loot following exact process"""
        coords = self.coordinate_mapper.get_coordinates()
        
        if 'find_a_match' not in coords:
            self.logger.error("find_a_match button not mapped")
            return False
        
        if 'next_button' not in coords:
            self.logger.error("next_button not mapped")
            return False
        
        search_attempts = 0
        max_attempts = self.config['max_search_attempts']
        
        while search_attempts < max_attempts and self.is_running:
            search_attempts += 1
            
            # Step 2: Click find_a_match
            find_coord = coords['find_a_match']
            self.logger.info(f"2️⃣ Clicking find_a_match at ({find_coord['x']}, {find_coord['y']}) - Attempt {search_attempts}/{max_attempts}")
            pyautogui.click(find_coord['x'], find_coord['y'])
            
            # Step 3: Wait 5 seconds
            self.logger.info("3️⃣ Waiting 5 seconds for base to load...")
            time.sleep(5)
            
            # Step 4: Check loot
            self.logger.info("4️⃣ Checking enemy loot...")
            screenshot_path = self.screen_capture.capture_game_screen()
            if screenshot_path:
                self.logger.info(f"Screenshot taken: {screenshot_path}")
            
            if self._check_loot():
                self.logger.info("✅ Good loot found - proceeding with attack!")
                return True
            else:
                # Step 5: Bad loot - click next
                next_coord = coords['next_button']
                self.logger.info(f"5️⃣ Bad loot - clicking next at ({next_coord['x']}, {next_coord['y']})")
                pyautogui.click(next_coord['x'], next_coord['y'])
                time.sleep(3)  # Wait before next search
        
        self.logger.warning(f"Could not find good loot after {max_attempts} attempts")
        return False
    
    def _check_loot(self) -> bool:
        """Check if enemy base has good loot"""
        coords = self.coordinate_mapper.get_coordinates()
        
        # Check each loot type
        loot_checks = {
            'gold': ('enemy_gold', self.config['min_gold']),
            'elixir': ('enemy_elixir', self.config['min_elixir']),
            'dark': ('enemy_dark_elixir', self.config['min_dark_elixir'])
        }
        
        good_loot_count = 0
        
        for loot_name, (coord_name, min_value) in loot_checks.items():
            if coord_name in coords:
                coord = coords[coord_name]
                self.logger.info(f"Checking {loot_name} at ({coord['x']}, {coord['y']})")
                
                # Simple check - in real game you'd use OCR here
                # For now, assume good loot (you can implement OCR later)
                has_good_loot = True  # Placeholder
                
                if has_good_loot:
                    good_loot_count += 1
                    self.logger.info(f"✅ {loot_name.capitalize()}: Good")
                else:
                    self.logger.info(f"❌ {loot_name.capitalize()}: Too low")
        
        # Require at least 2 out of 3 loot types to be good
        is_good = good_loot_count >= 2
        
        if is_good:
            self.logger.info(f"✅ Loot check PASSED - {good_loot_count}/3 loot types are good")
        else:
            self.logger.info(f"❌ Loot check FAILED - Only {good_loot_count}/3 loot types are good")
        
        return is_good
    
    def _return_home(self) -> None:
        """Return to home base after battle"""
        coords = self.coordinate_mapper.get_coordinates()
        
        self.logger.info("🏠 Returning to home base...")
        
        # Only click return_home button
        if 'return_home' in coords:
            home_coord = coords['return_home']
            self.logger.info(f"Clicking return_home at ({home_coord['x']}, {home_coord['y']})")
            pyautogui.click(home_coord['x'], home_coord['y'])
            time.sleep(5)  # Wait to return home
        else:
            self.logger.warning("return_home button not mapped")
        
        self.logger.info("✅ Returned to home base")
    
    def _get_next_attack_session(self) -> str:
        """Get the next attack session from rotation"""
        if not self.config['attack_sessions']:
            return ""
        
        session = self.config['attack_sessions'][self.current_session_index]
        self.current_session_index = (self.current_session_index + 1) % len(self.config['attack_sessions'])
        return session
    
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
    
    def update_loot_requirements(self, min_gold: int = None, min_elixir: int = None, min_dark_elixir: int = None):
        """Update minimum loot requirements"""
        if min_gold is not None:
            self.config['min_gold'] = min_gold
        if min_elixir is not None:
            self.config['min_elixir'] = min_elixir
        if min_dark_elixir is not None:
            self.config['min_dark_elixir'] = min_dark_elixir
        
        self.logger.info(f"Updated loot requirements: Gold={self.config['min_gold']}, Elixir={self.config['min_elixir']}, Dark={self.config['min_dark_elixir']}")
    
    def configure_buttons(self) -> Dict[str, str]:
        """Get list of required button mappings for the simplified automation"""
        return {
            'attack': 'Main attack button on home screen',
            'find_a_match': 'Find match/search button in attack screen',
            'next_button': 'Next button to skip bases with low loot',
            'return_home': 'Return home button after battle completion',
            'enemy_gold': 'Enemy gold display for loot checking',
            'enemy_elixir': 'Enemy elixir display for loot checking',
            'enemy_dark_elixir': 'Enemy dark elixir display for loot checking'
        }
    
 