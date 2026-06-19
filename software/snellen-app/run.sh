#!/bin/bash
cd "$(dirname "$0")"

# Activate venv — path differs between Windows (Git Bash) and Linux
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

python app.py
