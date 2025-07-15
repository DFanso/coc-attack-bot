#!/usr/bin/env python3
"""
COC Attack Bot - Main Entry Point
Automated Clash of Clans attack bot for Windows
"""

import sys
import os
from src.bot_controller import BotController
from src.ui.console_ui import ConsoleUI
from src.utils.logger import Logger

def main():
    """Main entry point for the COC Attack Bot"""
    try:
        # Initialize logger
        logger = Logger()
        logger.info("Starting COC Attack Bot...")
        
        # Initialize bot controller
        bot = BotController()
        
        # Initialize console UI
        ui = ConsoleUI(bot)
        
        # Start the application
        ui.run()
        
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 