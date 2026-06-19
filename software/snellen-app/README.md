# Snellen Visual Acuity Test App

Automated Snellen chart test displayed on an HDMI screen inside a VR headset. Patients read letters one at a time using voice input. Tests each eye separately and saves results as JSON.

## Hardware Required

- Laptop (runs the app)
- 7-inch HDMI screen (mounted in VR headset)
- Microphone (USB or built-in)
- VR headset enclosure with biconvex lens

## How It Works

1. Enter patient name
2. App instructs patient to cover one eye
3. Letters are shown one at a time, largest to smallest
4. Patient reads each letter aloud into the microphone
5. Speech recognition scores each response
6. Visual acuity (e.g. 20/20, 20/40) is calculated per eye
7. Results saved to `results/` as JSON

---

## Setup — Linux

```bash
cd snellen-app
./setup.sh
```

Run the app:
```bash
./run.sh
```

## Setup — Windows

Double-click `setup.bat` (first time only).

Run the app:
```
run.bat
```

---

## Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `DISPLAY_OFFSET_X` | `1920` | X position of HDMI screen |
| `DISPLAY_OFFSET_Y` | `0` | Y position of HDMI screen |
| `MIC_DEVICE_INDEX` | `0` | Microphone device index |
| `PASS_THRESHOLD` | `0.6` | Min correct per row to continue |
| `LISTEN_TIMEOUT` | `8` | Seconds to wait for voice response |

**Find your HDMI screen position:**

Linux:
```bash
xrandr --query
```

Windows: Settings → System → Display → scroll down to see monitor arrangement. The HDMI screen position in pixels is your `DISPLAY_OFFSET_X`.

**Find your microphone index:**
```bash
python -c "import speech_recognition as sr; [print(i, m) for i, m in enumerate(sr.Microphone.list_microphone_names())]"
```

---

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
      { "acuity": "20/200", "correct": 1, "total": 1, "accuracy": 1.0, "passed": true }
    ]
  }
}
```

---

## File Structure

```
snellen-app/
├── app.py          — main application
├── chart.py        — Snellen letter rows and acuity scores
├── speech.py       — microphone and speech recognition
├── config.py       — display and test settings
├── setup.sh        — first-time setup (Linux)
├── setup.bat       — first-time setup (Windows)
├── run.sh          — run the app (Linux)
├── run.bat         — run the app (Windows)
├── results/        — saved patient test results (JSON)
└── requirements.txt
```

## Notes

- Requires internet connection for Google Speech Recognition
- Font sizes in `chart.py` may need calibration based on your specific lens and screen
- The biconvex VR lens optically simulates the standard 6-meter Snellen testing distance
