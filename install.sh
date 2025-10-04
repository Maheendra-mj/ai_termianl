#!/bin/bash

echo ">>> Setting up AI Terminal..."

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Create a virtual environment
echo ">>> Creating virtual environment in 'venv'..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo ">>> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Install the ai-terminal package itself in editable mode
echo ">>> Installing the 'ai-terminal' command..."
pip install -e .

echo ""
echo "--------------------------------------------------"
echo "✅ Installation Complete!"
echo "--------------------------------------------------"
echo ""
echo "To run your new terminal, you must first:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Set your Gemini API Key: export GEMINI_API_KEY='YOUR_API_KEY_HERE'"
echo "3. Run the MCP Server in a separate terminal: uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000"
echo "4. Run your terminal: ai-terminal"
echo ""
