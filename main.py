from pathlib import Path
from core import llm_interface, automator
import json
import config
import os

def run():
    # --- 1. Setup ---
    # Use the setting from the config file
    COPILOT_NAME = config.ACTIVE_COPILOT 
    PROJECT_ROOT = Path(__file__).parent

    # --- 2. Get User Command ---
    print("--- AI Copilot for Legacy Systems ---")
    user_command = input("Please enter your command:\n> ")
    
    if not user_command:
        print("No command entered. Exiting.")
        return

    # --- 3. Generate Action Plan from LLM ---
    # This single function call does all the AI work
    action_plan = llm_interface.get_action_plan_from_llm(COPILOT_NAME, user_command)
    
    if action_plan:
        print("\n--- Generated Action Plan ---")
        # Pretty-print the JSON plan
        print(json.dumps(action_plan, indent=2))

        # --- 4. Execute the Plan ---
        # Save the generated plan to a temporary file for the automator
        temp_plan_path = PROJECT_ROOT / '_temp_plan.json'
        with open(temp_plan_path, 'w') as f:
            json.dump(action_plan, f, indent=2)

        ui_map_path = PROJECT_ROOT / 'copilots' / COPILOT_NAME / 'ui_map.json'
        print("\nAbout to execute the plan. Make sure the target application is visible and maximized.")
        input("Press Enter to continue...") # Gives the user a chance to prepare
        
        automator.execute_plan(ui_map_path, temp_plan_path)

        # Clean up the temporary file
        os.remove(temp_plan_path)
        print("\nExecution complete.")

    else:
        print("\nCould not generate a valid action plan. Please try rephrasing your command.")

if __name__ == '__main__':
    run()