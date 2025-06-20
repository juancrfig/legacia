from pathlib import Path
from core import llm_interface, automator
import json
import config

def run():
    # --- Use the setting from the config file ---
    COPILOT_NAME = config.ACTIVE_COPILOT 
    PROJECT_ROOT = Path(__file__).parent