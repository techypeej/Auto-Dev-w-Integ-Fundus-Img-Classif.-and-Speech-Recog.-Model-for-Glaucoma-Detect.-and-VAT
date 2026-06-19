@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing Python packages...
pip install SpeechRecognition

echo Installing PyAudio for Windows...
pip install pipwin
pipwin install pyaudio

echo.
echo Setup complete. Run the app with: run.bat
pause
