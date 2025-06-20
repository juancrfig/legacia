import os
import json
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

def get_action_plan_from_llm(copilot_name: str, user_command: str):
    """
    Generates a structured action plan from a user command using the LLM.
    
    Args:
        copilot_name: The name of the copilot package (e.g., 'genexus_legacy_vX').
        user_command: The natural language command from the user.

    Returns:
        A list of action dictionaries, or None if an error occurs.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("ERROR: GOOGLE_API_KEY not found. Please check your .env file.")
            return None
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Construct paths to copilot files
        project_root = Path(__file__).parent.parent
        copilot_dir = project_root / 'copilots' / copilot_name
        ui_map_path = copilot_dir / 'ui_map.json'
        prompt_template_path = copilot_dir / 'prompts.md'

        # Load the content
        with open(ui_map_path, 'r') as f:
            ui_map_str = f.read()
        
        with open(prompt_template_path, 'r') as f:
            prompt_template = f.read()

        # Assemble the final prompt
        final_prompt = (
            f"{prompt_template}\n\n"
            f"--- UI MAP ---\n"
            f"{ui_map_str}\n\n"
            f"--- USER COMMAND ---\n"
            f"User: \"{user_command}\"\n\n"
            f"--- ACTION PLAN JSON ---"
        )
        
        print("Sending request to LLM... (this may take a moment)")
        response = model.generate_content(final_prompt)
        
        print("LLM response received.")
        
        # Clean the response and parse the JSON
        # LLMs often wrap JSON in markdown backticks ```json ... ```
        response_text = response.text.strip().replace("```json", "").replace("```", "").strip()

        # A final check in case of stray text before the JSON
        if not response_text.startswith('['):
            response_text = '[' + response_text.split('[', 1)[1]
            
        action_plan = json.loads(response_text)
        return action_plan

    except Exception as e:
        print(f"An error occurred while communicating with the LLM: {e}")
        # In case of an error, also print the raw response for debugging
        if 'response' in locals():
            print("\n--- Raw LLM Response for Debugging ---")
            print(response.text)
        return None