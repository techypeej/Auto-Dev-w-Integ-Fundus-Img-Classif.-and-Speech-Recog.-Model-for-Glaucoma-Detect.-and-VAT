# ── Display Settings ──────────────────────────────────────────────────────────
# DISPLAY_OFFSET_X = 0     → shows on your main laptop screen (use for testing)
# DISPLAY_OFFSET_X = 1920  → shows on second HDMI screen (use for the VR headset)
#
# Find the right value on Linux:  xrandr --query
# Find the right value on Windows: Settings → System → Display → check monitor layout
DISPLAY_OFFSET_X = 0     # set to 1920 when the HDMI screen is connected
DISPLAY_OFFSET_Y = 0

# ── Microphone ────────────────────────────────────────────────────────────────
# List devices: python -c "import speech_recognition as sr; [print(i,m) for i,m in enumerate(sr.Microphone.list_microphone_names())]"
MIC_DEVICE_INDEX = 1     # 1 = Microphone (M-830) on this Windows PC

# ── Test Settings ─────────────────────────────────────────────────────────────
PASS_THRESHOLD = 0.6     # fraction of letters correct to pass a row and continue
LISTEN_TIMEOUT = 8       # seconds to wait for the patient to start speaking

# ── Eyes ──────────────────────────────────────────────────────────────────────
EYES = ["Left", "Right"]
