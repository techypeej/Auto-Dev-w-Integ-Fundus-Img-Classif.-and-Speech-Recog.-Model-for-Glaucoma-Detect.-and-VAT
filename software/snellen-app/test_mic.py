import speech_recognition as sr

print("Available microphones:")
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"  [{i}] {name}")

index = int(input("\nEnter device index to test (1 for M-830): "))

r = sr.Recognizer()
print(f"\nUsing device [{index}]. Say something...")

try:
    with sr.Microphone(device_index=index) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening... (speak now)")
        audio = r.listen(source, timeout=6, phrase_time_limit=4)

    print("Recognizing...")
    text = r.recognize_google(audio)
    print(f"You said: {text}")

except sr.WaitTimeoutError:
    print("No speech detected within 6 seconds.")
except sr.UnknownValueError:
    print("Could not understand audio.")
except sr.RequestError as e:
    print(f"Google API error: {e}")
except Exception as e:
    print(f"Error: {e}")
