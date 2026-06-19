# Snellen Visual Acuity Test App

Automated Snellen chart test displayed on an HDMI screen inside a VR headset. Patients read letters one at a time using voice input. Tests each eye separately and saves results as JSON.

## Hardware Required

- Laptop (runs the app)
- 7-inch HDMI screen (mounted in VR headset)
- Microphone (USB or built-in)
- VR headset enclosure with biconvex lens

## How It Works

1. Patient name is entered on screen
2. App instructs patient to cover one eye
3. Letters are shown one at a time, largest to smallest
4. Patient reads each letter aloud
5. Speech recognition scores the response
6. Visual acuity (e.g. 20/20, 20/40) is calculated for each eye
7. Results are saved to `results/` as JSON

## Quick Start (Without Docker)

**1. Install system dependency (once only):**
```bash
sudo apt-get install portaudio19-dev
```

**2. Set up virtual environment:**
```bash
cd snellen-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configure your display:**

Find your HDMI screen position:
```bash
xrandr --query
```

Edit `config.py` and set `DISPLAY_OFFSET_X` to match your HDMI screen's X position.

**4. Run:**
```bash
./run.sh
```

## Quick Start (With Docker)

**Allow Docker to use your display:**
```bash
xhost +local:docker
```

**Build and run:**
```bash
docker compose up --build
```

Results are saved to `./results/` on your host machine.

## Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `DISPLAY_OFFSET_X` | `1920` | X position of HDMI screen (from xrandr) |
| `DISPLAY_OFFSET_Y` | `0` | Y position of HDMI screen |
| `PASS_THRESHOLD` | `0.6` | Min correct per row to continue (60%) |
| `LISTEN_TIMEOUT` | `8` | Seconds to wait for voice response |

## Results Format

Each test is saved to `results/PatientName_YYYYMMDD_HHMMSS.json`:

```json
{
  "patient_name": "Juan Dela Cruz",
  "date": "2026-06-19T10:30:00",
  "results": {
    "Left": "20/40",
    "Right": "20/20"
  },
  "details": {
    "Left": [
      { "acuity": "20/200", "correct": 1, "total": 1, "accuracy": 1.0, "passed": true },
      ...
    ]
  }
}
```

## File Structure

```
snellen-app/
├── app.py          — main application
├── chart.py        — Snellen letter rows and acuity scores
├── speech.py       — microphone and speech recognition
├── config.py       — display and test settings
├── run.sh          — convenience run script
├── results/        — saved patient test results (JSON)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Notes

- Requires internet connection for Google Speech Recognition
- Font sizes in `chart.py` may need calibration based on your specific lens and screen setup
- The biconvex VR lens optically simulates the standard 6-meter Snellen testing distance
