# ── Display Settings ──────────────────────────────────────────────
# Find your HDMI screen offset by running: xrandr --query
# If your laptop screen is 1920px wide and HDMI is to the right:
DISPLAY_OFFSET_X = 1920
DISPLAY_OFFSET_Y = 0

# ── Microphone ────────────────────────────────────────────────────
# Run this to list devices: python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
# Set to the index of your microphone (0 = first/default mic)
MIC_DEVICE_INDEX = 0

# ── Test Settings ─────────────────────────────────────────────────
PASS_THRESHOLD = 0.6    # 60% correct per row to pass and continue
LISTEN_TIMEOUT = 8      # seconds to wait for patient to respond

# ── Eyes ──────────────────────────────────────────────────────────
EYES = ["Left", "Right"]
