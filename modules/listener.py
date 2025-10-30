import speech_recognition as sr
from pynput import keyboard
import threading
import sys
import termios
import tty

recognizer = sr.Recognizer()
mic = sr.Microphone()
recording = False

def mute_input():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old

def unmute_input(old):
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)

def record_audio():
    global recording
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        print("🧠 Processing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except Exception as e:
        print("Error:", repr(e))
    recording = False

def on_press(key):
    global recording
    if key == keyboard.KeyCode.from_char('w') and not recording:
        recording = True
        threading.Thread(target=record_audio).start()
    elif key == keyboard.Key.esc:
        print("👋 Exiting...")
        return False

def main():
    print("Hold W to talk. Release to process. Press ESC to quit.")
    old = mute_input()
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    finally:
        unmute_input(old)

main()