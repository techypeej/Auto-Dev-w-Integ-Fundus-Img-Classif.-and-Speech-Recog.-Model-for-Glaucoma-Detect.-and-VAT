"""
Automated Snellen Visual Acuity Test
One eye at a time, one letter at a time, voice input.

Run: python app.py
"""
import tkinter as tk
import json
import datetime
import threading
from pathlib import Path

from config import DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y, PASS_THRESHOLD, LISTEN_TIMEOUT, EYES, MIC_DEVICE_INDEX
from chart import SNELLEN_CHART
from speech import listen_for_letter

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


class SnellenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snellen Eye Test")
        self.root.configure(bg="white")
        self.root.geometry(f"800x600+{DISPLAY_OFFSET_X}+{DISPLAY_OFFSET_Y}")
        self.root.attributes("-fullscreen", True)
        self.root.resizable(False, False)

        self.patient_name = ""
        self.eye_results  = {}   # {"Left": "20/40", "Right": "20/20"}
        self.eye_details  = {}   # full row-by-row scores per eye

    # ── Utilities ────────────────────────────────────────────────────

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def label(self, text, size=28, bold=False, color="black", y=0.5):
        weight = "bold" if bold else "normal"
        tk.Label(
            self.root, text=text,
            font=("Helvetica", size, weight),
            bg="white", fg=color
        ).place(relx=0.5, rely=y, anchor="center")

    def button(self, text, command, y=0.7):
        tk.Button(
            self.root, text=text, command=command,
            font=("Helvetica", 20), bg="#333", fg="white",
            padx=30, pady=10, relief="flat", cursor="hand2"
        ).place(relx=0.5, rely=y, anchor="center")

    # ── Screens ──────────────────────────────────────────────────────

    def show_welcome(self):
        self.clear()
        self.label("Snellen Visual Acuity Test", size=36, bold=True, y=0.25)
        self.label("Enter patient name:", size=22, y=0.42)

        entry = tk.Entry(self.root, font=("Helvetica", 24), justify="center", width=20)
        entry.place(relx=0.5, rely=0.55, anchor="center")
        entry.focus()

        def start():
            name = entry.get().strip()
            if name:
                self.patient_name = name
                self.show_eye_instruction(eye_index=0)

        self.root.bind("<Return>", lambda e: start())
        self.button("Start Test", start, y=0.72)

    def show_eye_instruction(self, eye_index: int):
        if eye_index >= len(EYES):
            self.show_final_results()
            return

        eye = EYES[eye_index]
        other_eye = EYES[1 - eye_index]

        self.clear()
        self.label(f"Testing: {eye} Eye", size=34, bold=True, y=0.25)
        self.label(f"Please cover your {other_eye.upper()} eye", size=26, y=0.42)
        self.label("You will see one letter at a time.", size=20, color="#555", y=0.55)
        self.label("Say the letter out loud when you see it.", size=20, color="#555", y=0.63)
        self.button("I'm Ready", lambda: self.run_eye_test(eye_index), y=0.78)

    def run_eye_test(self, eye_index: int):
        eye = EYES[eye_index]
        row_scores = []
        last_passed_acuity = None

        for row in SNELLEN_CHART:
            correct_count = 0

            for letter in row["letters"]:
                result = self.test_one_letter(letter, row["font_size"], eye)
                if result:
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
                break   # stop at first failed row

        acuity = last_passed_acuity or "< 20/200"
        self.eye_results[eye] = acuity
        self.eye_details[eye]  = row_scores

        self.show_eye_result(eye, acuity, eye_index)

    def test_one_letter(self, letter: str, font_size: int, eye: str) -> bool:
        """Shows one letter, listens, returns True if correct."""
        result_holder = [None]

        def do_listen():
            spoken, raw = listen_for_letter(LISTEN_TIMEOUT, MIC_DEVICE_INDEX)
            result_holder[0] = (spoken, raw)
            self.root.event_generate("<<ListenDone>>")

        self.clear()

        # Eye label (small, top left)
        tk.Label(
            self.root, text=f"{eye} Eye",
            font=("Helvetica", 16), bg="white", fg="#aaa"
        ).place(x=20, y=20)

        # The letter
        tk.Label(
            self.root, text=letter,
            font=("Courier", font_size, "bold"),
            bg="white", fg="black"
        ).place(relx=0.5, rely=0.45, anchor="center")

        # Listening indicator
        mic_label = tk.Label(
            self.root, text="🎤 Listening...",
            font=("Helvetica", 18), bg="white", fg="#888"
        )
        mic_label.place(relx=0.5, rely=0.78, anchor="center")

        self.root.update()

        # Listen in background thread, poll until done
        threading.Thread(target=do_listen, daemon=True).start()
        while result_holder[0] is None:
            self.root.update()
            self.root.after(100)

        spoken, raw = result_holder[0] if result_holder[0] else (None, "timeout")
        correct = spoken == letter if spoken else False

        # Brief feedback flash
        self.show_feedback(letter, correct, spoken)

        return correct

    def show_feedback(self, expected: str, correct: bool, spoken: str | None):
        self.clear()
        color   = "#2ecc71" if correct else "#e74c3c"
        symbol  = "✓" if correct else "✗"
        heard   = f'You said: "{spoken}"' if spoken else "Not heard"

        tk.Label(
            self.root, text=symbol,
            font=("Helvetica", 120, "bold"),
            bg="white", fg=color
        ).place(relx=0.5, rely=0.42, anchor="center")

        tk.Label(
            self.root, text=heard,
            font=("Helvetica", 20),
            bg="white", fg="#555"
        ).place(relx=0.5, rely=0.72, anchor="center")

        self.root.update()
        self.root.after(1200)   # show feedback for 1.2 seconds
        self.root.update()

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

    # ── Save & Restart ────────────────────────────────────────────────

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

    # ── Run ──────────────────────────────────────────────────────────

    def run(self):
        self.show_welcome()
        self.root.mainloop()


if __name__ == "__main__":
    SnellenApp().run()
