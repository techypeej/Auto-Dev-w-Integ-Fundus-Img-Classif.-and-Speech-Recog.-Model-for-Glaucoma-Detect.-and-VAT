# Snellen Visual Acuity Test App

Automated Snellen chart test displayed on an HDMI screen inside a VR headset. Patients read letters one at a time using voice input. Tests each eye separately and saves results as JSON.

## Hardware Required

- Laptop (runs the app)
- 7-inch HDMI screen (mounted in VR headset)
- Microphone (USB or built-in) — M-830 condenser mic recommended
- VR headset enclosure with biconvex lens

## How It Works

1. Enter patient name
2. App instructs patient to cover one eye
3. Letters are shown one at a time, largest to smallest
4. Patient reads each letter aloud — or operator presses the key as fallback
5. Speech recognition scores each response
6. Visual acuity (e.g. 20/20, 20/40) is calculated per eye
7. Results saved to `results/` as JSON

---

## Setup — Linux (or Windows Git Bash)

```bash
cd snellen-app
./setup.sh
```

Run the app:
```bash
./run.sh
```

## Setup — Windows (Command Prompt)

Double-click `setup.bat` (first time only).

Run the app:
```
run.bat
```

---

## Microphone Setup

Do this every time you move to a new PC.

**Step 1 — activate the venv first:**
```bash
# Linux / Git Bash
source venv/bin/activate

# Windows cmd
venv\Scripts\activate
```

**Step 2 — list all detected microphones:**
```bash
python -c "import speech_recognition as sr; [print(i, m) for i, m in enumerate(sr.Microphone.list_microphone_names())]"
```

Example output:
```
0 Microsoft Sound Mapper - Input
1 Microphone (M-830)
2 Microsoft Sound Mapper - Output
...
```

**Step 3 — find your microphone index.** Look for your mic name in the list. Ignore outputs (speakers), ignore "Sound Mapper" entries. Pick the index of your actual mic.

**Step 4 — update `config.py`:**
```python
MIC_DEVICE_INDEX = 1   # change to your mic's index
```

**Step 5 — test it works:**
```bash
python test_mic.py
```

Type the index you found, say something, and confirm it prints back what you said. Only continue to the app after this test passes.

### Known device indexes (update as you go)

| PC | Microphone | Index |
|---|---|---|
| Paul John's laptop (Windows) | Microphone (M-830) | 1 |
| Thesis lab PC (Linux) | HDA Intel PCH: ALC236 Analog | 0 |

---

## Display Setup

**Testing on laptop only (no HDMI screen):**
```python
DISPLAY_OFFSET_X = 0   # window appears on main screen
```

**When using the VR HDMI screen:**
```python
DISPLAY_OFFSET_X = 1920  # or wherever your HDMI screen sits
```

Find the exact value:

Linux:
```bash
xrandr --query
# Look for your HDMI output and note the X offset (e.g. 1920x1080+1920+0 → offset is 1920)
```

Windows: Settings → System → Display → drag monitors to match physical layout → the second screen's left edge position is your `DISPLAY_OFFSET_X`.

**Press Escape** at any time to toggle fullscreen (useful during setup).

---

## Configuration (`config.py`) — Full Reference

| Setting | Description | Testing value | Production value |
|---|---|---|---|
| `DISPLAY_OFFSET_X` | X position of window | `0` | `1920` (or your HDMI offset) |
| `DISPLAY_OFFSET_Y` | Y position of window | `0` | `0` |
| `MIC_DEVICE_INDEX` | Microphone device index | depends on PC | depends on PC |
| `PASS_THRESHOLD` | Min fraction correct per row | `0.6` | `0.6` |
| `LISTEN_TIMEOUT` | Seconds to wait for speech | `8` | `8` |

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
├── app.py           — main application
├── chart.py         — Snellen letter rows and acuity scores
├── speech.py        — microphone and speech recognition
├── config.py        — display and mic settings (edit this per device)
├── test_mic.py      — standalone mic test (run this to verify mic before app)
├── setup.sh         — first-time setup (Linux / Git Bash)
├── setup.bat        — first-time setup (Windows cmd)
├── run.sh           — run the app (Linux / Git Bash)
├── run.bat          — run the app (Windows cmd)
├── results/         — saved patient test results (JSON)
└── requirements.txt
```

## Notes

- Requires internet connection — Google Speech Recognition sends audio to Google's servers
- If voice recognition fails, the operator can press the letter key on the keyboard as a fallback
- Font sizes in `chart.py` may need calibration based on your specific lens and screen distance
- The biconvex VR lens optically simulates the standard 6-meter Snellen testing distance
- `[speech] heard: '...'` is printed to the terminal every time Google returns a result — check this to debug recognition issues
