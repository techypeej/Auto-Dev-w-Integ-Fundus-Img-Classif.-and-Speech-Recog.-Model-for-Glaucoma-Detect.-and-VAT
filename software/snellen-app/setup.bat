@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing packages...
pip install SpeechRecognition
pip install pyaudio

echo.
echo Setup complete. Run the app with: run.bat
pause
