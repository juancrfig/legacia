import pyautogui
import json
import time
from pathlib import Path

# --- Configuration ---
# Set a pause between each pyautogui command to give the app time to react.
pyautogui.PAUSE = 0.5 

def load_json_file(file_path):
    """A simple helper to load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def get_coords_from_id(ui_map, element_id):
    """
    Parses an element_id like 'window_kb_creation.button_create'
    and finds its coordinates in the ui_map.
    """
    try:
        keys = element_id.split('.')
        current_element = ui_map['elements']
        for key in keys:
            current_element = current_element[key]
        
        return current_element['coords']
    except KeyError:
        print(f"Error: Element ID '{element_id}' not found in the UI map.")
        return None

def execute_plan(ui_map_path, plan_path):
    """Loads the UI map and an action plan, then executes the plan."""
    
     # --- PRE-FLIGHT CHECK ---
    print("--- Performing Pre-flight Checks ---")
    required_dir = Path("C:/Models") # Use forward slashes, pathlib handles it correctly
    
    # Check if the path exists and is a directory
    if not required_dir.is_dir():
        print(f"Required directory '{required_dir}' not found. Creating it now.")
        try:
            # Create the directory. 'exist_ok=True' prevents errors if it was somehow created
            # in the meantime. 'parents=True' creates any needed parent folders too.
            required_dir.mkdir(parents=True, exist_ok=True)
            print("Directory created successfully.")
        except Exception as e:
            # Catch potential permission errors
            print(f"FATAL ERROR: Could not create directory '{required_dir}'.")
            print(f"Reason: {e}")
            print("Please create this directory manually and run the script again.")
            return # Stop execution if we can't create the folder
    else:
        print(f"Directory '{required_dir}' found. Check passed.")
    # --- END PRE-FLIGHT CHECK ---

    print("Loading UI map...")
    ui_map = load_json_file(ui_map_path)
    
    print("Loading action plan...")
    action_plan = load_json_file(plan_path)

    print("--- Starting Automation in 3 seconds. Please focus the GeneXus window. ---")
    time.sleep(3)

    for action in action_plan:
        action_type = action.get('action')
        print(f"Executing action: {action_type}")

        if action_type == 'click':
            coords = get_coords_from_id(ui_map, action['element_id'])
            if coords:
                pyautogui.click(coords[0], coords[1])

        elif action_type == 'type':
            coords = get_coords_from_id(ui_map, action['element_id'])
            if coords:
                pyautogui.click(coords[0], coords[1]) # Click to focus the field first
                time.sleep(0.2) # Small pause to ensure focus is set
                    
                # --- NEW: Clear the field ---
                pyautogui.hotkey('ctrl', 'a') # Select all text in the field
                pyautogui.press('delete')     # Delete the selected text
                time.sleep(0.2) # Pause to ensure deletion is processed
           
                pyautogui.write(action['text'], interval=0.1)

        elif action_type == 'hotkey':
            keys = action['keys'].split('+') # 'ctrl+shift+n' -> ['ctrl', 'shift', 'n']
            pyautogui.hotkey(*keys)

        else:
            print(f"Warning: Unknown action type '{action_type}'")
        
        # A small pause after each action to ensure the UI can keep up
        time.sleep(0.5)

    print("--- Automation plan finished! ---")


if __name__ == '__main__':
    # --- 2. Build absolute paths from the script's location ---

    # Get the directory of the current script (e.g., /path/to/project/core)
    SCRIPT_DIR = Path(__file__).parent 

    # Get the root directory of the project (e.g., /path/to/project)
    # .parent moves up one level from /core to the root.
    PROJECT_ROOT = SCRIPT_DIR.parent

    # --- 3. Define file paths using the project root ---
    # This now builds a reliable, absolute path regardless of where you run the script from.
    UI_MAP_FILE = PROJECT_ROOT / 'copilots' / 'genexusEv3' / 'ui_map.json'
    PLAN_FILE = PROJECT_ROOT / 'test_plan.json'
    
    # Don't forget to update the name of your genexus folder! 
    # For example: 'genexusEv3' if that's what you named it.
    
    # Now, we pass these Path objects to our function.
    # The `open()` function in load_json_file understands Path objects perfectly.
    execute_plan(UI_MAP_FILE, PLAN_FILE)