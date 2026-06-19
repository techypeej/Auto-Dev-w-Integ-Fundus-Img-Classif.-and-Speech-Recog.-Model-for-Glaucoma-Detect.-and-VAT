import speech_recognition as sr
from typing import Optional, Tuple

# Maps everything Google might return → the Snellen letter it means.
# Single letters are hard for Google STT — it returns rhyming words instead
# (e.g. saying "E" out loud → Google returns "he", "me", "we", "be", etc.)
SPOKEN_MAP = {
    # C
    "C": "C", "SEE": "C", "CEE": "C", "SEA": "C", "SI": "C",

    # D
    "D": "D", "DEE": "D", "DI": "D",

    # E — all words that rhyme with or sound like "E"
    "E": "E", "EE": "E",
    "HE": "E", "ME": "E", "WE": "E", "BE": "E",
    "GEE": "E", "LEE": "E", "FEE": "E", "KEY": "E",
    "TREE": "E", "FREE": "E", "THREE": "E", "THE": "E",

    # F
    "F": "F", "EF": "F", "EFF": "F",

    # L
    "L": "L", "EL": "L", "ELL": "L", "ELLE": "L",
    "HELL": "L", "WELL": "L", "BELL": "L", "FELL": "L",

    # O
    "O": "O", "OH": "O", "OWE": "O", "OHH": "O",
    "GO": "O", "NO": "O", "SO": "O", "LOW": "O", "KNOW": "O",

    # P
    "P": "P", "PEE": "P", "PE": "P",

    # T
    "T": "T", "TEE": "T", "TEA": "T", "TI": "T",

    # Z
    "Z": "Z", "ZEE": "Z", "ZED": "Z", "ZI": "Z",
}


def listen_for_letter(timeout: int = 8, device_index: int = 0) -> Tuple[Optional[str], str]:
    r = sr.Recognizer()
    # Do NOT set energy_threshold before adjust_for_ambient_noise —
    # adjust_for_ambient_noise will override it. Set it after, or skip calibration.
    r.dynamic_energy_threshold = True   # adapts to ambient noise in real time

    with sr.Microphone(device_index=device_index) as source:
        # Calibrate to room noise, then clamp so it isn't set too high
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.energy_threshold = min(r.energy_threshold, 400)  # cap so quiet voices still register

        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return None, "timeout"

    try:
        text = r.recognize_google(audio).upper().strip()
    except sr.UnknownValueError:
        return None, "unclear"
    except sr.RequestError as e:
        return None, f"api error: {e}"

    print(f"[speech] heard: {text!r}")  # always visible in terminal for debugging

    # Check every word Google returned against the map
    for word in text.split():
        if word in SPOKEN_MAP:
            return SPOKEN_MAP[word], text

    # Single character fallback
    if len(text) == 1 and text in SPOKEN_MAP:
        return SPOKEN_MAP[text], text

    return None, text
