import google.generativeai as genai
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()

def get_action_plan_from_llm(copilot_name: str, user_command: str) -> list | None:
    """
    Connects to the LLM to generate an action plan based on the UI map and user command.

    Args:
        copilot_name: The name of the copilot to use (e.g., 'my_app').
        user_command: The user's instruction.

    Returns:
        A list of actions (the plan) if successful, otherwise None.
    """
    # --- 1. Set the correct model name ---
    # This is the model name you confirmed works with your API key.
    MODEL_NAME = "models/gemini-1.5-flash-latest" 
    
    # --- 2. Load copilot assets (UI map and prompt) ---
    try:
        PROJECT_ROOT = Path(__file__).parent.parent # Goes up from 'core' to the project root
        copilot_dir = PROJECT_ROOT / 'copilots' / copilot_name
        ui_map_path = copilot_dir / 'ui_map.json'
        prompt_path = copilot_dir / 'prompts.md'

        with open(ui_map_path, 'r') as f:
            ui_map_content = f.read()
        with open(prompt_path, 'r') as f:
            prompt_content = f.read()

    except FileNotFoundError as e:
        print(f"Error: Could not find a required copilot file. {e}")
        return None

    # --- 3. Connect to the Google AI API ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return None
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        # --- 4. Construct the full prompt and get the response ---
        full_prompt = f"{prompt_content}\n\n---\n\nUI Map:\n{ui_map_content}\n\n---\n\nUser Command:\n{user_command}"
        
        print("\nSending request to the AI...")
        response = model.generate_content(full_prompt)
        
        # --- 5. Clean and parse the JSON response ---
        # The response can sometimes include markdown formatting (```json ... ```)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-4]
        
        return json.loads(response_text)

    except json.JSONDecodeError:
        print("\nError: The AI did not return a valid JSON plan.")
        print("Received:\n", response.text)
        return None
    except Exception as e:
        print(f"\nAn API error occurred: {e}")
        return None