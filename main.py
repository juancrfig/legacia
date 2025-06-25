# main.py

from pathlib import Path
from core import llm_interface, automator
import json
import config
import os

def run():
    # --- 1. Setup and Initialize Conversation ---
    COPILOT_NAME = config.ACTIVE_COPILOT
    PROJECT_ROOT = Path(__file__).parent

    print("--- AI Copilot for Legacy Systems ---")
    print("Initializing chat session... This may take a moment.")
    
    # Start the conversation. This sends the rules and UI map just once.
    session_id = llm_interface.start_chat_session(COPILOT_NAME)
    
    if not session_id:
        print("Failed to initialize chat session. Exiting.")
        return

    # --- 2. Command Loop ---
    while True:
        user_command = input("\nEnter your command (or type 'exit' to quit):\n> ")
        
        if user_command.lower() == 'exit':
            print("Exiting copilot.")
            break
            
        if not user_command:
            print("No command entered.")
            continue

        # --- 3. Generate Action Plan from LLM (using the existing session) ---
        action_plan = llm_interface.get_action_plan_from_llm(session_id, user_command)
        
        if action_plan:
            print("\n--- Generated Action Plan ---")
            print(json.dumps(action_plan, indent=2))

            # --- 4. Execute the Plan ---
            temp_plan_path = PROJECT_ROOT / '_temp_plan.json'
            with open(temp_plan_path, 'w') as f:
                json.dump(action_plan, f, indent=2)

            ui_map_path = PROJECT_ROOT / 'copilots' / COPILOT_NAME / 'ui_map.json'
            
            print("\nAbout to execute the plan. Make sure the target application is visible and maximized.")
            input("Press Enter to continue...")
            
            automator.execute_plan(ui_map_path, temp_plan_path)

            os.remove(temp_plan_path)
            print("\nExecution complete.")

        else:
            print("\nCould not generate a valid action plan. Please try rephrasing your command.")

if __name__ == '__main__':
    run()