# core/llm_interface.py

import google.generativeai as genai
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import uuid

# Load API Key from .env file
load_dotenv()

# --- State Management ---
# A simple dictionary to hold active chat sessions.
# In a larger application, you might use a more robust session management system.
ACTIVE_SESSIONS = {}

def start_chat_session(copilot_name: str) -> str:
    """
    Starts a new chat session with the initial system prompt and UI map.

    Args:
        copilot_name: The name of the copilot to use.

    Returns:
        A unique session ID string for this chat session.
    """
    # --- 1. Load copilot assets (UI map and prompt) ---
    try:
        PROJECT_ROOT = Path(__file__).parent.parent
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

    # --- 2. Construct the initial system prompt ---
    initial_prompt = f"{prompt_content}\n\n---\n\nUI Map:\n{ui_map_content}\n\n---\n\nFrom now on, I will only provide the User Command. Generate the JSON action plan based on these rules and the UI map."

    # --- 3. Configure the API and Model ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

        # --- 4. Start the chat ---
        chat = model.start_chat(history=[
            {'role': 'user', 'parts': [initial_prompt]},
            {'role': 'model', 'parts': ["OK. I am ready. Please provide the first user command."]}
        ])
        
        # --- 5. Store the session and return its ID ---
        session_id = str(uuid.uuid4())
        ACTIVE_SESSIONS[session_id] = chat
        
        print("✅ Chat session initialized successfully.")
        return session_id

    except Exception as e:
        print(f"\nAn API error occurred during initialization: {e}")
        return None


def get_action_plan_from_llm(session_id: str, user_command: str) -> list | None:
    """
    Sends a user command to an existing chat session and gets the action plan.

    Args:
        session_id: The ID of the active chat session.
        user_command: The user's instruction.

    Returns:
        A list of actions (the plan) if successful, otherwise None.
    """
    chat = ACTIVE_SESSIONS.get(session_id)
    if not chat:
        print("Error: Invalid session ID.")
        return None
        
    try:
        print("\nSending command to the AI...")
        response = chat.send_message(user_command)
        
        # --- Clean and parse the JSON response ---
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-4] # Remove markdown code block
        
        return json.loads(response_text)

    except json.JSONDecodeError:
        print("\nError: The AI did not return a valid JSON plan.")
        print("Received:\n", response.text)
        return None
    except Exception as e:
        print(f"\nAn API error occurred: {e}")
        return None