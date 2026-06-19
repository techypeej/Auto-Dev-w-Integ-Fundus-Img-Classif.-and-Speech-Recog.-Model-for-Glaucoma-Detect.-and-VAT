import speech_recognition as sr
from typing import Optional, Tuple

# Maps spoken words → Snellen letters
SPOKEN_MAP = {
    "C": "C", "SEE": "C", "CEE": "C",
    "D": "D", "DEE": "D",
    "E": "E", "EE": "E",
    "F": "F", "EF": "F", "EFF": "F",
    "L": "L", "EL": "L", "ELL": "L",
    "N": "N", "EN": "N",
    "O": "O", "OH": "O", "ZERO": "O",
    "P": "P", "PEE": "P",
    "T": "T", "TEE": "T",
    "Z": "Z", "ZEE": "Z", "ZED": "Z",
}


def listen_for_letter(timeout: int = 8, device_index: int = 0) -> Tuple[Optional[str], str]:
    """
    Listens for a single spoken letter.
    Returns (matched_letter, raw_text).
    matched_letter is None if unrecognized or timed out.
    """
    r = sr.Recognizer()
    r.energy_threshold = 300

    with sr.Microphone(device_index=device_index) as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            return None, "timeout"

    try:
        text = r.recognize_google(audio).upper().strip()
    except sr.UnknownValueError:
        return None, "unclear"
    except sr.RequestError:
        return None, "mic error"

    # Try full text first, then first word
    for candidate in [text, text.split()[0] if text.split() else ""]:
        if candidate in SPOKEN_MAP:
            return SPOKEN_MAP[candidate], text

    # Single character fallback
    if len(text) == 1 and text in SPOKEN_MAP:
        return text, text

    return None, text
