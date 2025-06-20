# Legacia

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Status: Active](https://img.shields.io/badge/status-active-success.svg)](https://github.com/juancrfig/legacia)

A reusable, AI-powered framework to automate interactions with legacy systems through natural language commands, effectively creating a "copilot" for software that lacks modern APIs.

## The Core Problem

Many of us work with older legacy systems (like specific versions of GeneXus, SAP, AS/400, etc.) where performing even simple tasks requires navigating complex, unintuitive menus. This manual, repetitive work is inefficient and drains cognitive energy that could be better spent on high-value tasks. This project aims to solve that problem systemically.

## How It Works: The Vision

The library allows a user to issue commands in natural language (e.g., *"Create a new client transaction for Acme Corp."*), which an AI then translates into a series of GUI automation steps (mouse clicks, keyboard inputs) to execute the task on your behalf.

The architecture is modular, with a "copilot package" for each supported legacy application.

### Core Components of a Copilot Package:

1.  **`ui_map.json`**: The "world model." A structured JSON file that maps the entire UI of the legacy application, defining the location and properties of all relevant buttons, menus, and fields.
2.  **`prompts.md`**: A collection of sophisticated LLM prompts designed to translate high-level user intent into a specific sequence of actions based on the `ui_map.json`.
3.  **`automator.py`**: An automation script (e.g., using `pyautogui`) that receives a structured action plan from the LLM and executes the GUI manipulations.
4.  **`llm_interface.py`**: A module to handle communication with a chosen Large Language Model API (e.g., GPT-4, Claude, Gemini).

## Project Status & Roadmap

This project is currently in the initial development phase.

### MVP (Starter Plan)
- [ ] **1. UI Mapping:** Manually map the essential UI of a target legacy system (starting with GeneXus) into the first `ui_map.json`.
- [ ] **2. Prompt Engineering:** Write initial prompts to handle 2-3 common, repetitive tasks.
- [ ] **3. Automation Scripting:** Implement a basic UI automation script using `pyautogui`.
- [ ] **4. Integration:** Develop the Python "glue code" to connect all the components into a working prototype.

### Long-Term Vision
*   Build a personal, reusable library of copilots for various legacy systems.
*   Refine the framework into a toolkit that can be easily adapted by other developers.
*   Create a standout portfolio piece showcasing expertise in system architecture, AI integration, and practical automation.

## Getting Started

*(This section will be updated as the project progresses)*

## Contributing
Contributions are welcome and wanted! This project is for anyone who has ever been frustrated by legacy software.
You can contribute in several ways:
- Report Bugs: If you find a bug, please open an issue.
- Suggest Features: Have an idea to make this better? Open an issue to discuss it.
- Create a Copilot Package: Map the UI of a legacy system you work with and submit a pull request.
- Improve the Code: Refactor code, improve automation scripts, or enhance the LLM interface.

Please fork the repository and create a pull request with your changes.

### License
This project is distributed under the MIT License. See the LICENSE file for more information.
