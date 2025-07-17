"""
Main entry point for the Hologram Tuning application.
Initializes the GUI and starts the application event loop.

compiler Setting
 -> pyinstaller -w -F --icon=".\resource\logo.ico" --name Sine_Maker source\main.py
if you used uv, try the next command. 
    uv lock
    uv sync
elif you used pip, follow the next step. 
    pip install PySide6
#!/usr/bin/env python3
"""

import sys
import logging
from pathlib import Path
from typing import NoReturn
from PySide6.QtWidgets import QApplication

# Add parent directory to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from source.mainControl import MainController

def setup_logging() -> None:
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def app() -> NoReturn:
    """
    Initialize and run the main application.
    
    Sets up the Qt application, creates the main controller,
    and starts the event loop.
    """
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting CLUT")
        
        app = QApplication(sys.argv)
        controller = MainController()
        controller.show_main_view()
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)

# if __name__ == '__main__':
#     main()
