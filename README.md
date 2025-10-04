AI Terminal Project
This project creates a powerful, AI-assisted hybrid terminal. It consists of a backend "MCP Server" that processes natural language and a custom, installable "AI Terminal" client that you run locally.

Features
Hybrid Terminal: Run standard shell commands (ls, git, etc.) and AI commands from the same interface.

AI-Powered Commands: Type ? followed by a task in plain English (e.g., ? find all files larger than 50MB) to get a suggested shell command.

Client-Server Architecture: The heavy lifting of AI processing is handled by a separate FastAPI server.

Persistent History: All executed commands are saved to a local SQLite database.

Installable Application: The terminal is packaged as a proper Python application and can be installed with a simple script, creating an ai-terminal command.

How to Install
Clone the repository:

git clone <your-repo-url>
cd ai_terminal_project

Make the installer executable:

chmod +x install.sh

Run the installer:

./install.sh

This will create a virtual environment, install all dependencies, and make the ai-terminal command available within that environment.

How to Use
You need two terminals open to run the system.

Terminal 1: Run the MCP Server

Activate the virtual environment:

source venv/bin/activate

Set your Gemini API Key:

export GEMINI_API_KEY='YOUR_API_KEY_HERE'

Start the server:

uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000

Leave this terminal running.

Terminal 2: Run the AI Terminal Client

Activate the virtual environment:

source venv/bin/activate

Launch your terminal:

ai-terminal

Using the Terminal Interface

For a standard command: Just type it and press Enter.

➤ ls -l

For an AI command: Start with ? and describe your task.

➤ ? find all markdown files and count their lines
