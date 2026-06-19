#!/bin/bash
# First-time setup for Linux
echo "Installing system dependency..."
sudo apt-get install -y portaudio19-dev

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "Setup complete. Run the app with: ./run.sh"
