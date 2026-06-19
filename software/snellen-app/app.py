"""
Automated Snellen Visual Acuity Test
One eye at a time, one letter at a time, voice input.

Run (Linux/Windows Git Bash): ./run.sh
Run (Windows cmd):            run.bat

Keyboard fallback: if voice isn't recognized, the operator can press the
letter key on the keyboard during the listening screen.
Press Escape to toggle fullscreen (useful during testing).
"""
import tkinter as tk
import json
import datetime
import threading
import time
from pathlib import Path
from typing import Optional

from config import DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y, PASS_THRESHOLD, LISTEN_TIMEOUT, EYES, MIC_DEVICE_INDEX
from chart import SNELLEN_CHART
from speech import listen_for_letter

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

FONT = "Arial"


class SnellenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snellen Eye Test")
        self.root.configure(bg="white")
        self.root.geometry(f"800x600+{DISPLAY_OFFSET_X}+{DISPLAY_OFFSET_Y}")
        self.root.attributes("-fullscreen", True)

        # Escape toggles fullscreen — useful during testing
        self.root.bind("<Escape>", lambda e: self.root.attributes(
            "-fullscreen", not self.root.attributes("-fullscreen")
        ))

        self.patient_name = ""
        self.eye_results  = {}
        self.eye_details  = {}

    # ── Utilities ──────────────────────────────────────────────────────

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def label(self, text, size=28, bold=False, color="black", y=0.5):
        weight = "bold" if bold else "normal"
        tk.Label(
            self.root, text=text,
            font=(FONT, size, weight),
            bg="white", fg=color
        ).place(relx=0.5, rely=y, anchor="center")

    def button(self, text, command, y=0.7):
        tk.Button(
            self.root, text=text, command=command,
            font=(FONT, 20), bg="#333", fg="white",
            padx=30, pady=10, relief="flat", cursor="hand2"
        ).place(relx=0.5, rely=y, anchor="center")

    def pause(self, seconds: float):
        end = time.time() + seconds
        while time.time() < end:
            self.root.update()
            time.sleep(0.05)

    # ── Screens ────────────────────────────────────────────────────────

    def show_welcome(self):
        self.clear()
        self.label("Snellen Visual Acuity Test", size=36, bold=True, y=0.22)
        self.label("Enter patient name:", size=22, y=0.40)

        entry = tk.Entry(self.root, font=(FONT, 24), justify="center", width=20)
        entry.place(relx=0.5, rely=0.52, anchor="center")
        entry.focus()

        def start():
            name = entry.get().strip()
            if name:
                self.patient_name = name
                self.show_eye_instruction(eye_index=0)

        self.root.bind("<Return>", lambda e: start())
        self.button("Start Test", start, y=0.70)

    def show_eye_instruction(self, eye_index: int):
        if eye_index >= len(EYES):
            self.show_final_results()
            return

        eye       = EYES[eye_index]
        other_eye = EYES[1 - eye_index]

        self.clear()
        self.label(f"Testing: {eye} Eye", size=34, bold=True, y=0.22)
        self.label(f"Cover your {other_eye.upper()} eye", size=26, y=0.38)
        self.label("One letter will appear at a time.", size=20, color="#555", y=0.52)
        self.label("Say it out loud — or press its key.", size=20, color="#555", y=0.60)
        self.button("I'm Ready", lambda: self.run_eye_test(eye_index), y=0.76)

    def run_eye_test(self, eye_index: int):
        eye = EYES[eye_index]
        row_scores = []
        last_passed_acuity = None

        for row in SNELLEN_CHART:
            correct_count = 0

            for letter in row["letters"]:
                if self.test_one_letter(letter, row["font_size"], eye):
                    correct_count += 1

            accuracy = correct_count / len(row["letters"])
            passed   = accuracy >= PASS_THRESHOLD

            row_scores.append({
                "acuity":   row["acuity"],
                "correct":  correct_count,
                "total":    len(row["letters"]),
                "accuracy": round(accuracy, 2),
                "passed":   passed,
            })

            if passed:
                last_passed_acuity = row["acuity"]
            else:
                break

        acuity = last_passed_acuity or "< 20/200"
        self.eye_results[eye] = acuity
        self.eye_details[eye] = row_scores
        self.show_eye_result(eye, acuity, eye_index)

    def test_one_letter(self, letter: str, font_size: int, eye: str) -> bool:
        result_holder = [None]

        # ── Voice listener in background thread ──
        def do_listen():
            try:
                spoken, raw = listen_for_letter(LISTEN_TIMEOUT, MIC_DEVICE_INDEX)
                if result_holder[0] is None:
                    result_holder[0] = ("voice", spoken, raw)
            except Exception as e:
                if result_holder[0] is None:
                    result_holder[0] = ("voice", None, f"mic error: {e}")

        # ── Keyboard fallback: operator presses the letter ──
        def on_key(event):
            if not event.char:
                return
            key = event.char.upper()
            if key.isalpha() and len(key) == 1 and result_holder[0] is None:
                result_holder[0] = ("keyboard", key, f"keyboard:{key}")

        self.root.bind("<Key>", on_key)

        # ── Build listening screen ──
        self.clear()

        tk.Label(
            self.root, text=f"{eye} Eye",
            font=(FONT, 16), bg="white", fg="#aaa"
        ).place(x=20, y=20)

        tk.Label(
            self.root, text=letter,
            font=("Courier New", font_size, "bold"),
            bg="white", fg="black"
        ).place(relx=0.5, rely=0.42, anchor="center")

        status_label = tk.Label(
            self.root, text="",
            font=(FONT, 18), bg="white", fg="#888"
        )
        status_label.place(relx=0.5, rely=0.75, anchor="center")

        hint_label = tk.Label(
            self.root,
            text="Say the letter aloud  |  or press its key on keyboard",
            font=(FONT, 13), bg="white", fg="#bbb"
        )
        hint_label.place(relx=0.5, rely=0.85, anchor="center")

        self.root.update()
        threading.Thread(target=do_listen, daemon=True).start()

        # ── Poll: update countdown, accept keyboard, wait for result ──
        start_time = time.time()
        while result_holder[0] is None:
            elapsed   = time.time() - start_time
            remaining = max(0, LISTEN_TIMEOUT - elapsed + 0.5)  # +0.5 for calibration
            status_label.config(text=f"[ Listening... {remaining:.0f}s ]")
            self.root.update()
            time.sleep(0.1)

        self.root.unbind("<Key>")

        _, spoken, raw = result_holder[0]
        correct = (spoken == letter) if spoken else False
        self.show_feedback(letter, correct, spoken, raw)
        return correct

    def show_feedback(self, expected: str, correct: bool, spoken: Optional[str], raw: str = ""):
        self.clear()
        color  = "#2ecc71" if correct else "#e74c3c"
        symbol = "CORRECT" if correct else "WRONG"

        # Result
        tk.Label(self.root, text=symbol,
                 font=(FONT, 64, "bold"), bg="white", fg=color
                 ).place(relx=0.5, rely=0.25, anchor="center")

        # Expected letter
        tk.Label(self.root, text=f"Expected:  {expected}",
                 font=(FONT, 24, "bold"), bg="white", fg="#222"
                 ).place(relx=0.5, rely=0.46, anchor="center")

        # What Google actually returned (raw) — most important for debugging
        tk.Label(self.root, text=f'Google heard:  "{raw}"',
                 font=(FONT, 20), bg="white", fg="#555"
                 ).place(relx=0.5, rely=0.58, anchor="center")

        # What it matched to (or didn't)
        if spoken:
            match_text  = f"Matched as:  {spoken}"
            match_color = "#2ecc71" if correct else "#e74c3c"
        else:
            match_text  = "No match found — add this word to SPOKEN_MAP in speech.py"
            match_color = "#e74c3c"

        tk.Label(self.root, text=match_text,
                 font=(FONT, 16), bg="white", fg=match_color
                 ).place(relx=0.5, rely=0.70, anchor="center")

        self.root.update()
        self.pause(3.0)  # 3 seconds so you can read what happened

    def show_eye_result(self, eye: str, acuity: str, eye_index: int):
        self.clear()
        self.label(f"{eye} Eye Result", size=32, bold=True, y=0.25)
        self.label(acuity, size=72, bold=True, color="#2c3e50", y=0.48)

        next_index = eye_index + 1
        if next_index < len(EYES):
            next_label = f"Continue to {EYES[next_index]} Eye"
        else:
            next_label = "View Final Results"
        self.button(next_label, lambda: self.show_eye_instruction(next_index), y=0.75)

    def show_final_results(self):
        self.clear()
        self.label("Test Complete", size=34, bold=True, y=0.15)
        self.label(f"Patient: {self.patient_name}", size=22, color="#555", y=0.27)

        y = 0.42
        for eye, acuity in self.eye_results.items():
            self.label(f"{eye} Eye:  {acuity}", size=30, bold=True, y=y)
            y += 0.14

        self.save_results()
        self.label("Results saved.", size=16, color="#aaa", y=0.78)
        self.button("New Patient", self.restart, y=0.88)

    # ── Save & Restart ─────────────────────────────────────────────────

    def save_results(self):
        record = {
            "patient_name": self.patient_name,
            "date":         datetime.datetime.now().isoformat(),
            "results":      self.eye_results,
            "details":      self.eye_details,
        }
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = RESULTS_DIR / f"{self.patient_name}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(record, f, indent=2)

    def restart(self):
        self.patient_name = ""
        self.eye_results  = {}
        self.eye_details  = {}
        self.show_welcome()

    def run(self):
        self.show_welcome()
        self.root.mainloop()


if __name__ == "__main__":
    SnellenApp().run()
