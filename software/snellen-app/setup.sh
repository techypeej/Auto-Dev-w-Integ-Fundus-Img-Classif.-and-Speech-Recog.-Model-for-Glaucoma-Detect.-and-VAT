#!/bin/bash
cd "$(dirname "$0")"

# Install system dependency (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing portaudio (Linux)..."
    sudo apt-get install -y portaudio19-dev
fi

echo "Creating virtual environment..."
python3 -m venv venv 2>/dev/null || python -m venv venv

# Activate venv — path differs between Windows (Git Bash) and Linux
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installing packages..."
pip install SpeechRecognition pyaudio

echo ""
echo "Setup complete. Run the app with: ./run.sh"
