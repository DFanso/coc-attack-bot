"""
Screen Capture Module - Handles screen capture and game window detection
"""

import pyautogui
import cv2
import numpy as np
import time
import os
from typing import Optional, Tuple, List
from datetime import datetime
import win32gui
import win32con

class ScreenCapture:
    """Handles screen capture and game window detection"""
    
    def __init__(self):
        self.screenshot_dir = "screenshots"
        self.game_window_title = "Clash of Clans"
        self.game_window_bounds = None
        
        # Create screenshots directory
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def find_game_window(self) -> Optional[Tuple[int, int, int, int]]:
        """Find the COC game window and return its bounds (x, y, width, height)"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "clash of clans" in window_title.lower() or "bluestacks" in window_title.lower() or "nox" in window_title.lower():
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append((hwnd, window_title, rect))
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            # Take the first match
            hwnd, title, rect = windows[0]
            x, y, right, bottom = rect
            width = right - x
            height = bottom - y
            self.game_window_bounds = (x, y, width, height)
            print(f"Found game window: {title} at ({x}, {y}, {width}, {height})")
            return self.game_window_bounds
        
        print("Could not find COC game window. Make sure the game is running.")
        return None
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """
        Capture screenshot of specified region or full screen
        Returns the path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        if region:
            # Capture specific region
            screenshot = pyautogui.screenshot(region=region)
        else:
            # Capture full screen or game window if detected
            if self.game_window_bounds:
                screenshot = pyautogui.screenshot(region=self.game_window_bounds)
            else:
                screenshot = pyautogui.screenshot()
        
        screenshot.save(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath
    
    def capture_game_screen(self) -> Optional[str]:
        """Capture screenshot of the game window specifically"""
        if not self.game_window_bounds:
            self.find_game_window()
        
        if self.game_window_bounds:
            return self.capture_screen(self.game_window_bounds)
        return None
    
    def find_template_on_screen(self, template_path: str, threshold: float = 0.8, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
        """
        Find a template image on screen using template matching
        Returns the center coordinates of the match if found
        """
        # Take screenshot
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Convert to OpenCV format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Load template
        if not os.path.exists(template_path):
            print(f"Template not found: {template_path}")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # Calculate center coordinates
            template_height, template_width = template.shape[:2]
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            
            # Adjust for region offset if specified
            if region:
                center_x += region[0]
                center_y += region[1]
            
            return (center_x, center_y)
        
        return None
    
    def wait_for_template(self, template_path: str, timeout: int = 30, threshold: float = 0.8, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
        """
        Wait for a template to appear on screen
        Returns coordinates when found or None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            coords = self.find_template_on_screen(template_path, threshold, region)
            if coords:
                return coords
            time.sleep(0.5)
        
        print(f"Template not found within timeout: {template_path}")
        return None
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get the RGB color of a pixel at specified coordinates"""
        screenshot = pyautogui.screenshot()
        pixel = screenshot.getpixel((x, y))
        return pixel
    
    def save_template(self, region: Tuple[int, int, int, int], name: str) -> str:
        """Save a region of the screen as a template for later matching"""
        template_dir = "templates"
        os.makedirs(template_dir, exist_ok=True)
        
        screenshot = pyautogui.screenshot(region=region)
        filepath = os.path.join(template_dir, f"{name}.png")
        screenshot.save(filepath)
        
        print(f"Template saved: {filepath}")
        return filepath 