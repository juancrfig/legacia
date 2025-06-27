# main.py

from pathlib import Path
from core import llm_interface, automator
import json
import config
import os
from gui import CopilotGUI
import threading
import pygetwindow as gw
import time

GENEXUS_WINDOW_TITLE = 'GeneXus'  # Partial match for window title

class CopilotApp:
    def __init__(self):
        self.COPILOT_NAME = config.ACTIVE_COPILOT
        self.PROJECT_ROOT = Path(__file__).parent
        self.session_id = None
        self.current_plan_path = None
        self.ui_map_path = self.PROJECT_ROOT / 'copilots' / self.COPILOT_NAME / 'ui_map.json'
        self.gui = CopilotGUI(self.on_send)

    def start(self):
        print("--- AI Copilot for Legacy Systems ---")
        print("Initializing chat session... This may take a moment.")
        self.session_id = llm_interface.start_chat_session(self.COPILOT_NAME)
        if not self.session_id:
            print("Failed to initialize chat session. Exiting.")
            return
        self.gui.mainloop()

    def on_send(self, user_command):
        # Run LLM call in a background thread to avoid freezing the GUI
        threading.Thread(target=self._generate_and_handle_plan, args=(user_command,), daemon=True).start()

    def _generate_and_handle_plan(self, user_command):
        if not isinstance(self.session_id, str):
            print("Session ID is invalid. Please restart the application.")
            return
        action_plan = llm_interface.get_action_plan_from_llm(self.session_id, user_command)
        if action_plan:
            print("\n--- Generated Action Plan ---")
            print(json.dumps(action_plan, indent=2))
            temp_plan_path = self.PROJECT_ROOT / '_temp_plan.json'
            with open(temp_plan_path, 'w') as f:
                json.dump(action_plan, f, indent=2)
            self.current_plan_path = temp_plan_path
            # Disable GUI controls (must be done in main thread)
            self.gui.root.after(0, lambda: self.gui.set_disabled(True))
            # Focus GeneXus and execute the plan in a thread
            threading.Thread(target=self._focus_and_execute, daemon=True).start()
        else:
            print("\nCould not generate a valid action plan. Please try rephrasing your command.")

    def _focus_and_execute(self):
        focus_genexus()
        time.sleep(0.5)  # Give a moment for focus to switch
        if self.current_plan_path is not None:
            automator.execute_plan(self.ui_map_path, self.current_plan_path)
            os.remove(str(self.current_plan_path))
        print("\nExecution complete.")
        self.gui.set_disabled(False)

def focus_genexus():
    windows = gw.getWindowsWithTitle(GENEXUS_WINDOW_TITLE)
    for w in windows:
        try:
            w.activate()
            return
        except Exception:
            continue

if __name__ == '__main__':
    app = CopilotApp()
    app.start()