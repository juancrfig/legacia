from pathlib import Path
from core import llm_interface, automator
import json
import config

def run():
    # --- Use the setting from the config file ---
    COPILOT_NAME = config.ACTIVE_COPILOT 
    PROJECT_ROOT = Path(__file__).parent

    # --- Get User Command ---
    print("--- AI Copilot for Legacy Systems ---")
    user_command = input("Please enter your command:\n> ")
    
    if not user_command:
        print("No command entered. Exiting.")
        return

    # --- Generate Action Plan from LLM ---
    action_plan = llm_interface.get_action_plan_from_llm(COPILOT_NAME, user_command)
    
    if action_plan:
        print("\n--- Generated Action Plan ---")
        for i, action in enumerate(action_plan, 1):
            print(f"{i}: {action}")

        # Save the generated plan to a temporary file for the automator
        temp_plan_path = PROJECT_ROOT / '_temp_plan.json'
        with open(temp_plan_path, 'w') as f:
            json.dump(action_plan, f, indent=2)

        # --- Execute the Plan ---
        ui_map_path = PROJECT_ROOT / 'copilots' / COPILOT_NAME / 'ui_map.json'
        print("\nAbout to execute the plan. Make sure the application is maximized.")
        automator.execute_plan(ui_map_path, temp_plan_path)

    else:
        print("\nCould not generate a valid action plan. Please try rephrasing your command.")

if __name__ == '__main__':
    run()    